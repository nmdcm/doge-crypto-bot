# doge-crypto-bot
A telegram bot that returns the latest cryptocurrency data based on the various parameters specified. 
Price, Stats and News data are provided by the [Binance](https://binance-docs.github.io/apidocs/spot/en/#change-log), [CoinMarketCap](https://coinmarketcap.com/api/) and [CryptoPanic](https://cryptopanic.com/developers/api/) APIs respectively.
The bot also uses WebSockets to allow for a higher amount of efficiency.

1.<b> /price</b> returns the latest price at which a trade occured between the specified coin and USDT.
<p align="center">
<img width="414" alt="price" src="https://user-images.githubusercontent.com/51364789/114159809-41231000-9937-11eb-8af6-ab785384abe2.png">
</p>
2.<b> /stats</b> returns the latest market data captured of the specified coin.
 
<p align="center">
<img width="414" alt="stats" src="https://user-images.githubusercontent.com/51364789/114159815-42ecd380-9937-11eb-8ff1-579c4915ecc8.png">
</p>
3.<b> /news</b> returns the latest news of a specified coin. If a coin is not specified /news will return the top stories of the cryptocurrency market.

<p align="center">
<img width="414" alt="news" src="https://user-images.githubusercontent.com/51364789/114159722-22bd1480-9937-11eb-9bd2-5961de308281.png">
</p>

The bot is available on [Telegram](https://t.me/DoggeCoinBot). Please allow for a minute for the bot to wake up as it goes to sleep after 30 mins of inactivity.
