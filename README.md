# Covid19

This is a Coronavirus-19 dashboard. Our focus for this project was to look for evidence suggesting that the vaccine may prevent people from being carriers of the Coronavirus-19. 

The Flask folder contains an app.py that has routes to the HTML pages. Line charts contain the average new confirmed cases vs time, the average new deceased people vs time, the running sum of new deceased people vs time, and the running sum of new people fully vaccinated vs time. The scatter chart has the global running sum of new people fully vaccinated on the x-axis and the global average new confirmed daily cases on the y-axis. For the bar chart the top ten countries that are closest to fully vaccinating their entire population are displayed. The heatmap shows the running sum of new people fully vaccinated by latitude and longitude from the beginning of 2021 to the current day. Example pictures are included below:

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/avg_new_confirmed_cases_per_day.PNG)

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/avg_new_deaths_per_day.PNG)

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/cum_deaths_over_time.PNG)

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/cum_new_people_vaxxed_over_time.PNG)

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/scatterchart.PNG)

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/barchart.PNG)

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/heatmap.PNG)

After looking through the visualizations you can see that some of the data suggests the vaccines are effective at preventing people from being carriers. For the top ten countries that are closest to fully vaccinating their population you can see how their respective average new cases per day line charts are starting to increase at a less extreme rate or even decrease in some cases. For example:

![Image description](https://github.com/sebastiandifrancesco/Covid19/blob/main/Images/evidence.PNG)
