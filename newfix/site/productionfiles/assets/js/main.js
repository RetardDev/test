console.log("check")
    
// fetch("/config/")
// .then((result) => {return result.json();})
// .then((data) => {
//     const stripe = Stripe(data.publicKey)

//     document.querySelector("#submitBtn").addEventListener("click", () => {
//         const selectedServiceStripeId = document.querySelector("selectServiceStripeId").ariaValueMax;
//         fetch("/create-checkout-session/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify({selectedServiceStripeId}),
//         })
//         .then((result) => { return result.json(); })
//         .then((data) => {
//             console.log(data);
//             return stripe.redirectToCheckout({sessionId: data.sessionId})
//         })
//         .then((res) => {
//             console.log(res);
//         });
//     });
// });