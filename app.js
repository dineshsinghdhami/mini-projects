const apiKey = "8d05ffb75ecbf746ffc119d5b3f713bf"; // API key for OpenWeatherMap 

document.getElementById("weatherForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const city = document.getElementById("cityInput").value.trim();
    const result = document.getElementById("result");

    if (city === "") {
        result.innerHTML = "Please enter city name";
        return;
    }

    result.innerHTML = "Loading...";

    try {
        const res = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
        );

        const data = await res.json();

        if (Number(data.cod) !== 200) {
            result.innerHTML = "City not found";
            return;
        }

        result.innerHTML = `
            <h2>${data.name}</h2>
            <p>${Math.round(data.main.temp)}°C</p>
            <p>${data.weather[0].description}</p>
            <p>Humidity: ${data.main.humidity}%</p>
            <p>Wind: ${Math.round(data.wind.speed)} km/h</p>
        `;

    } catch (error) {
        result.innerHTML = "Error loading weather";
    }
});