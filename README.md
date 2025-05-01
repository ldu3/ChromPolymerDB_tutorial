# ChromPolymerDB_tutorial

<!-- ABOUT THE PROJECT -->
The spatial organization of the genome plays a fundamental role in gene regulation, replication, and other biological processes. High-throughput chromosome conformation capture (Hi-C) techniques have advanced our understanding of genome architecture, but they primarily produce 2D, population-averaged data, limiting insights into individual cell chromatin structures. To bridge this gap, this project introduces a computational method and web-based platform designed for high-resolution visualization and analysis of single-cell 3D chromatin conformations.

<img src="image/main_page.png" alt="Main Page" title="Main Page" width="1000" />

<!-- GETTING STARTED -->
## Step 1. Querying the Data

- Our database provides two ways to query the Hi-C data:
  1. Based on the cell line name and genomic location.

     <img src="image/data_query_short.png" alt="data_query" title="data_query" width="1000" />
     
  2. Based on the cell line name and gene name.

     <img src="image/data_query_gene_short.png" alt="data_query" title="data_query" width="1000" />

After entering all the information, click the <code style="color : Cyan">Show Heatmap</code>
<!-- GETTING STARTED -->
## Step 2. Examine the FoldRec interactions

Here we take IMR90 chr8:127,300,000-128,300,000 as an example.

<img src="image/FoldRec_1_full.png" alt="FoldRec" title="FoldRec" width="600" />

- The upper panel showed the selected cell line and region. 
   - The tool buttons on the right are:
      - Restore the original heatmap
      - Expand the heatmap view
      - Download FoldRec interaction data
      - Generate the 3D single-cell structures 
- The middle panel showed the chromatin interactions heatmap. 
   - The upper triangle of the heatmap shows the FoldRec inteactions and the lower triangle of the heatmap shows the experiment Hi-C data. The color scale represent the interaction frequency. 
   - Users can change the color scale using the slide bar on the right.
   - Users can click and drag the heatmap to zoom in and out.
- The lower panel showed the gene information in this region, users can select and click the gene to highlight it. Here we select MYC gene.

#### By clicking  <img src="image/expand_button.png" alt="button" title="button" width="20" />  (Expand the heatmap view). We can check the FoldRec interactions in details with epigentic tracks from ENCODE

<img src="image/FoldRec2_full.png" alt="FoldRec" title="FoldRec" width="600" />

- The upper panel showed the tool buttons:
   - Scale bar to change the heatmap color scale 
   - Swith button to swich between FoldRec interactions and All HiC data
   - Tracks button to select epigenitic tracks from ENCODE or uplode local files
   - Downlode the figures
- The middle panel showed the FoldRec interactions. Users can click the heatmap to highlight selected interations
- The lower panel is the igv epigenitic tracks. Users can select epigenitc tracks they are interested in to annotate the biological meaning of the interactions

<!-- GETTING STARTED -->
## Step 3. Generating the 3D single-cell chromatin structures

After examining the FoldRec interactions, users can click  <img src="image/3D_Structure.png" alt="button" title="button" width="80" />  to generate the 3D single-cell chromatin structures

<img src="image/single_cell_conformation.png" alt="FoldRec" title="FoldRec" width="600" />

<!-- GETTING STARTED -->
## Step 4. 
