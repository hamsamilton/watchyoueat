library(ggplot2)

df <- rio::import("/Users/samuelhamilton/Downloads/foodtrack_mhealth_class.csv")#[,c(4:10,14:16)]

sr <- df %>% 
  filter(!is.na(full)) 
  cor() 
heatmap

prcomp(sr)
ggbiplot(prcomp(sr))
pca()
dat <- sr
## reshape data (tidy/tall form)
dat2 <- dat %>%
  tbl_df() %>%
  rownames_to_column('Var1') %>%
  gather(Var2, value, -Var1) %>%
  mutate(
    Var1 = factor(Var1, levels=1:10),
    Var2 = factor(gsub("V", "", Var2), levels=1:10)
  )

## plot data
ggplot(s, aes(Var1, Var2)) +
  geom_tile(aes(fill = value)) + 
  geom_text(aes(label = round(value, 1))) +
  scale_fill_gradient(low = "white", high = "red") 


sr <- jit
autoplot(prcomp(sr),loadings = TRUE, loadings.colour = 'blue',
         loadings.label = TRUE, loadings.label.size = 3)



kdf <- df[,8:10]
####
kdf <- kdf %>% 
  mutate(no = rownames(df)) %>% 
  pivot_longer(cols = names(df)[8:10]) 

kdf <- kdf[,2:3]

ggplot(kdf, aes(x = name,y = value,fill = name)) +
  geom_violin() +
  labs(x= "Question Category",
       y = "Self-reported value",
       fill = "Question Category")



kdf <- df[,1:7]
####l
kdf <- kdf %>% 
  mutate(no = rownames(df)) %>% 
  pivot_longer(cols = names(df)[1:7]) 

kdf <- kdf[,2:3]

ggplot(kdf, aes(x = name,y = value,fill = name)) +
  geom_violin() +
  labs(x= "Question Category",
       y = "Self-reported value",
       fill = "Question Category")
l

lm1 <- lm(overeat ~ urge + hungry + stressed + sad + happy + energized + distracted, data = df)
anova(lm1)

lm2 <- lm(full ~ urge + hungry + stressed + sad + happy + energized + distracted, data = df)
anova(lm2)

lm3 <- lm(control_loss ~ urge + hungry + stressed + sad + happy + energized + distracted, data = df)
anova(lm3)


sjt.
