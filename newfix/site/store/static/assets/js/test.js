


console.log("check")
    



fetch("/config/")
.then((result) => {return result.json();})
.then((data) => {
    const stripe = Stripe(data.publicKey)

    document.querySelector("#submitBtn").addEventListener("click", () => {
        const selectedServiceStripeId = document.querySelector("#selectedServiceStripeId").value;
        var address = document.getElementById('address').value
        var phone = document.getElementById('phone').value
       
        // if(!isValidAddress(address)){
        //     console.error('Invalid address');
        //     return;
        // }
        // if(!isValidPhone(phone)){
        //     console.error('Invalid phone number');
        //     return;
        // }


        fetch("/create-checkout-session/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({address: address, phone: phone, selectedServiceStripeId: selectedServiceStripeId, }),
        })
        .then((result) => { return result.json(); })
        .then((data) => {
            console.log(data);
            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
            console.log(res);
        });
    });
});

// function isValidAddress(address){

//     //google map api street verfication

//     return address.trim() !== '';
// }

// function isValidPhone(phone){

//     //add more phone verfication such as country

//     return /^\d{10}$/.test(phone);
// }