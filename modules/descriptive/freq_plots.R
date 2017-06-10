

#Mostrar el punch card, dias de la semana vs hours, on circulos, the circle size is the frequency
#ggplot(mydata100, aes(pretest, posttest)) +geom_point()

library(ggplot2) 
library(scales)

# Meses
month_counts_mails <- read.csv("~/dpa-equipo-10/Proyecto/modules/descriptive/month_counts_mails.csv",header=FALSE)
colnames(month_counts_mails) <- c("Mes","Freq")

ggplot(month_counts_mails, aes(Mes, Freq)) + 
  geom_bar(colour="black", stat="identity", position=position_dodge(), size=.3) +
  xlab("") + ylab("Daily")


# Diario
date_counts_querys <- read.csv("~/dpa-equipo-10/Proyecto/modules/descriptive/date_counts_querys.csv",header=FALSE)
nrow(date_counts_querys)
colnames(date_counts_querys) <- c("Dia","Freq")
date_counts_querys$Tipo <- 'Queries'

date_counts_mails <- read.csv("~/dpa-equipo-10/Proyecto/modules/descriptive/date_counts_mails.csv",header=FALSE)
nrow(date_counts_mails)
colnames(date_counts_mails) <- c("Dia","Freq")
date_counts_mails$Tipo <- 'Mails'

date_counts <- rbind(date_counts_querys, date_counts_mails)

date_counts$Dia <- as.Date(date_counts$Dia)
date_counts$Year <- format(date_counts$Dia, "%Y")
date_counts$Month <- format(date_counts$Dia, "%b")
date_counts$Day <- format(date_counts$Dia, "%d")
date_counts$MonthDay <- format(date_counts$Dia, "%d-%b")
#date_counts <- date_counts_mails[date_counts$Year>=2014,]

ggplot(data = date_counts,
      mapping = aes(x = date_counts$Dia, y = date_counts$Freq,  shape = Tipo, colour = Tipo)) + 
      geom_line() +  xlab("") + ylab("Frecuencia")




##ya no se usa
#ggplot(data = date_counts_mails,
#       mapping = aes(x = CommonDate, y = Y, shape = Year, colour = Year)) +
  #geom_point() +
#  geom_line() +
#  facet_grid(facets = Year ~ .) +
#  scale_x_date(labels = function(x) format(x, "%d-%b"))




