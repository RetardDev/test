console.log("check")
    
fetch("/config/")
.then((result) => {return result.json();})
.then((data) => {
    const stripe = Stripe(data.publicKey)

    document.querySelector("#submitBtn").addEventListener("click", () => {
        const address = document.querySelector("#address").value
        const phone = document.querySelector("#phone").value
            fetch("/create-checkout-session-M/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({address, phone})
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