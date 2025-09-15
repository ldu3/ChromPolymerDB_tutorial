setwd("C:/Users/11543/Desktop/database/Calu3")

#load the position data
Calu3_pos <- read.csv("Calu3_chr8_127200000_127750000.csv")

#each batch contains 5000 samples
#n_cycles <- nrow(Calu3_pos) / 110
n_cycles <- 5000   

#choose the target beads
#0 based 3,19,40,61,77,94,107
rel_idx <- c(4,20,41,62,78,95,108)
target_rows <- unlist(lapply(0:(n_cycles - 1), function(i) i * 110 + rel_idx))

Calu3_pos_target_rows <- Calu3_pos[target_rows,]
#id,x,y,z
Calu3_pos_target_rows <- Calu3_pos_target_rows[,c(4,7,8,9)]


#euclidean distance
euclidean_dist <- function(p1, p2) {
  sqrt(sum((p1 - p2)^2))
}

#collect sampleid
sample_ids <- unique(Calu3_pos_target_rows$sampleid)


distance_list <- list()
for (sid in sample_ids) {
  points <- Calu3_pos_target_rows[Calu3_pos_target_rows$sampleid == sid, c("x", "y", "z")]
  #all enhancers (1:6) vs TSS (7)
  combs <- combn(c(1:6,7), 2)
  combs_with_7 <- combs[, apply(combs, 2, function(x) 7 %in% x)]
  dists <- apply(combs_with_7, 2, function(idx) {
    euclidean_dist(points[idx[1], ], points[idx[2], ])
  })
  distance_list[[as.character(sid)]] <- dists
}

# print each result
distance_list[["3110"]] 


library(dplyr)
dist_df <- do.call(rbind, lapply(names(distance_list), function(sid) {
  data.frame(sampleid = as.integer(sid),
             pair = paste0("(", c(1:6), ",", 7, ")"),
             distance = distance_list[[sid]])
}))

# multi contacts
dist_df_close <- dist_df[dist_df$distance<80 + 34.3,]
dist_df_close$first_pair <- as.numeric(gsub("\\((\\d+),.*", "\\1", dist_df_close $pair))
dist_df_close_new <- dist_df_close %>%
  group_by(sampleid) %>%
  summarise(
    unique_firsts = paste(unique(first_pair), collapse = ","),
    count = n()
  )

