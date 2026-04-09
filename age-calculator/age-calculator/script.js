let dateOfBirth = document.querySelector("#DOB");
const CalcAge = document.getElementById("CalcAge");
const Age = document.getElementById("age");

CalcAge.addEventListener("click", () => {
    let dobValue = dateOfBirth.value;

    if (!dobValue) {
        Age.innerText = "Please select your date of birth!";
        Age.style.color = "red";
        return;
    }

    let birthDate = new Date(dobValue);
    let today = new Date();

    let age = today.getFullYear() - birthDate.getFullYear();
    let m = today.getMonth() - birthDate.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age -= 1;
    }

    Age.innerText = `You are ${age} years old.`;
    Age.style.color = "green";
});
