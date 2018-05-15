library(htmltab)
df905 = htmltab("https://en.wikipedia.org/wiki/Progressive_Conservative_Party_of_Ontario_leadership_election,_2018",12)
dfTO  = htmltab("https://en.wikipedia.org/wiki/Progressive_Conservative_Party_of_Ontario_leadership_election,_2018",11)
dfEO  = htmltab("https://en.wikipedia.org/wiki/Progressive_Conservative_Party_of_Ontario_leadership_election,_2018",13)
dfSWO  = htmltab("https://en.wikipedia.org/wiki/Progressive_Conservative_Party_of_Ontario_leadership_election,_2018",14)
dfNO  = htmltab("https://en.wikipedia.org/wiki/Progressive_Conservative_Party_of_Ontario_leadership_election,_2018",15)

VarNames = c('Riding', 'B1Allan', 'B1Elliott', 'B1Ford', 'B1Mulruney', 'B1Total', 
             'B2Elliott','B2ElliottChange', 'B2Ford','B2FordChange', 'B2Mulruney','B2MulruneyChange', 'B2Total', 'B2TotalChange',
             'B3Elliott','B3ElliottChange', 'B3Ford','B3FordChange', 'B3Total','B3TotalChange')


colnames(df905) = VarNames
colnames(dfTO) = VarNames
colnames(dfEO) = VarNames
colnames(dfSWO) = VarNames
colnames(dfNO) = VarNames

library(tidyverse)
df = rbind(df905, dfTO, dfEO, dfSWO, dfNO)


# Cleaning.
df$Riding <- str_replace(df$Riding,"\\:.*","")
df$Riding <- str_replace(df$Riding,"MPP","")
df$Riding <- str_replace(df$Riding,"MP","")
df$Riding <- str_replace(df$Riding,"Candidate","")

df <- df[!duplicated(df$Riding), ]
splitVars = c('Total', 'Change')

names <- df %>% 
  select(-contains("Total"), -contains('Change'), -Riding) %>% 
  names()




smallerDF <-  df %>% 
  select(-contains("Total"), -contains('Change'))

smallerDF = smallerDF %>%
  gather(Ballot, value, -Riding) %>% 
  separate(value, c('Percent', 'Votes'), sep = '[(]') %>% 
  gather(Type, value, - Riding, -Ballot ) %>% 
  unite(var, Ballot, Type) %>% 
  spread(var, value)


braceRemover <- function(df){
  for (colName in names(df)){
    if (grepl('[)]', df[, colName])){
      df[, colName] = gsub("[)]", "", df[[colName]]) %>% as.numeric()
    }
  }
  return(df)
}

smallerDF <- braceRemover(smallerDF)

write_csv(smallerDF, '/Users/kailukowiak/DATA_608/FPApp/RidingData.csv')
