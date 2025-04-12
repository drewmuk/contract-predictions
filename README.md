# contract-predictions

Machine learning project to predict the total contract value of upcoming NBA free agents (2025 offseason). I scraped data from Spotrac and Basketball-Reference, then selected features I believed would be most important in informing contract value (basic per-game stats as well as PER, WS, VORP, usage rate, and games played). I added information about the league-wide salary cap each year, awards, and whether a player won a championship each year. Each row contains a unique contract, the player’s statistics, awards, and championships for the past three seasons before they signed that contract, their age at the time, and the salary cap that offseason.

With this dataframe, I used an XGBoost model to predict total contract value. I fit the model on my training data and calculated the accuracy of its predictions on the test set using the mean absolute difference between prediction and actual value. Finally, I read in the CSV with the upcoming off-season’s free agents. After merging with 2025’s per-game and advanced statistics (for which there was nearly a full season of data as of March 30) and the salary cap for 2025-26, I just needed to add awards, and championships for 2025. LeBron James, Kyrie Irving, and James Harden were named to the all-star team in February, and I am projecting that LeBron James will be named to the All-NBA second team. No free agents in this upcoming class are contenders for other awards, based on sportsbook betting odds. I used the betting odds to estimate championship probabilities for each team and linked those with the free agents’ current teams to complete the 2025 variables. The top 5 in my predictions in order were Kyrie Irving, LeBron James, James Harden, John Collins, and Jonathan Kuminga.
