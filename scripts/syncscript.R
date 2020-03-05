library(ggplot2)
df <- rio::import("/Users/samuelhamilton/watchyoueat/data/Necklace/Sam 3_3_20/necklace_data.csv")
offset <- -140000
df$elantime <- df$Time + offset 
df$Time <- df$Time - df$Time[1] + offset
df$time <- df$Time - df$Time[1] + offset
write.csv(df,"/Users/samuelhamilton/watchyoueat/data/Necklace/Sam 3_3_20/fixednecklace_data.csv",row.names = F)
#ggplot(df,aes(x = elantime,y = proximity)) + geom_point()
