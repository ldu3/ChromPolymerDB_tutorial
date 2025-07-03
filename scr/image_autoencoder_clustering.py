import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization, Flatten, Dense, Reshape
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# -------------------------------
# 1) Set Up Paths and Parameters
# -------------------------------
IMAGE_DIR = "./image_png/"             # Folder containing your images
IMG_HEIGHT, IMG_WIDTH = 64, 64   # Resize images to 64x64 (adjust as needed)
IMG_CHANNELS = 3                 # Use 3 for RGB images
LATENT_DIM = 128                 # Increase latent dimension for richer features
BATCH_SIZE = 32
EPOCHS = 100                     # Train for more epochs to let the loss drop
LEARNING_RATE = 1e-4             # Lower learning rate for fine adjustments

# -------------------------------
# 2) Load and Preprocess Images
# -------------------------------
def load_and_preprocess_image(image_path, target_size=(IMG_WIDTH, IMG_HEIGHT)):
    # Open the image, convert to RGB, resize it, and normalize to [0,1]
    img = Image.open(image_path).convert('RGB').resize(target_size)
    img_array = np.array(img, dtype='float32') / 255.0
    return img_array  # Shape: (IMG_HEIGHT, IMG_WIDTH, 3)

# Get list of image paths and load images.
image_paths = [os.path.join(IMAGE_DIR, fname) for fname in os.listdir(IMAGE_DIR)
               if fname.lower().endswith(('.png', '.jpg', '.jpeg'))]
images = np.array([load_and_preprocess_image(path) for path in image_paths])
print("Images shape:", images.shape)  # Expected: (n_samples, 64, 64, 3)

# -------------------------------
# 3) Build a Modified Convolutional Autoencoder
# -------------------------------
input_img = Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))

# Encoder
# Block 1
x = Conv2D(32, (3,3), activation='relu', padding='same')(input_img)
x = BatchNormalization()(x)
x = MaxPooling2D((2,2), padding='same')(x)
# Block 2
x = Conv2D(64, (3,3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2,2), padding='same')(x)
# Block 3
x = Conv2D(128, (3,3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
x = MaxPooling2D((2,2), padding='same')(x)
# For a 64x64 input, after 3 poolings the spatial dimensions are 8x8.
flat = Flatten()(x)
latent = Dense(LATENT_DIM, activation='relu')(flat)

# Decoder
# Calculate flat size from encoder output: 8 * 8 * 128 = 8192.
flat_size = 8 * 8 * 128
x = Dense(flat_size, activation='relu')(latent)
x = Reshape((8, 8, 128))(x)
# Decoder Block 1
x = UpSampling2D((2,2))(x)  # Now 16x16
x = Conv2D(128, (3,3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
# Decoder Block 2
x = UpSampling2D((2,2))(x)  # Now 32x32
x = Conv2D(64, (3,3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
# Decoder Block 3
x = UpSampling2D((2,2))(x)  # Now 64x64
x = Conv2D(32, (3,3), activation='relu', padding='same')(x)
x = BatchNormalization()(x)
# Final reconstruction layer
decoded = Conv2D(IMG_CHANNELS, (3,3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)
optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
autoencoder.compile(optimizer=optimizer, loss='binary_crossentropy')
autoencoder.summary()

# -------------------------------
# 4) Train the Autoencoder
# -------------------------------
history = autoencoder.fit(images, images,
                          epochs=EPOCHS,
                          batch_size=BATCH_SIZE,
                          shuffle=True,
                          validation_split=0.1)

# Plot training and validation loss.
plt.figure(figsize=(8,6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.show()

# -------------------------------
# 5) Extract Latent Features Using the Encoder
# -------------------------------
encoder_model = Model(input_img, latent)
latent_features = encoder_model.predict(images)
print("Latent features shape:", latent_features.shape)  # Expected: (n_samples, LATENT_DIM)

# -------------------------------
# 6) Determine the Optimal Number of Clusters Using Silhouette Score
# -------------------------------
cluster_range = range(2, 11)  # Try cluster counts from 2 to 10
sil_scores = []
for k in cluster_range:
    kmeans_temp = KMeans(n_clusters=k, random_state=42)
    labels_temp = kmeans_temp.fit_predict(latent_features)
    sil = silhouette_score(latent_features, labels_temp)
    sil_scores.append(sil)
    print(f"k={k}: Silhouette Score = {sil:.4f}")
optimal_k = cluster_range[sil_scores.index(max(sil_scores))]
print("Optimal number of clusters (Silhouette Score):", optimal_k)

# -------------------------------
# 7) Cluster the Extracted Features with K-means
# -------------------------------
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
final_labels = kmeans.fit_predict(latent_features)
print("Final cluster labels:", final_labels)

# -------------------------------
# 8) Save the Features and Clustering Info as a CSV File
# -------------------------------
n_features = latent_features.shape[1]
feature_columns = [f'feature_{i}' for i in range(n_features)]
df = pd.DataFrame(latent_features, columns=feature_columns)
df['cluster'] = final_labels
df['filename'] = [os.path.basename(path) for path in image_paths]
csv_filename = "custom_autoencoder_features.csv"
df.to_csv(csv_filename, index=False)
print("Saved features and clustering info to", csv_filename)

