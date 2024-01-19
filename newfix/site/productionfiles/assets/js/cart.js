
console.log("check")
    
fetch("/config/")
.then((result) => {return result.json();})
.then((data) => {
    const stripe = Stripe(data.publicKey)

    document.querySelector("#submitBtn").addEventListener("click", () => {

        var address = document.getElementById('address').value
        var phone = document.getElementById('phone').value

        // if(!isValidAddress(address)){
        //     showErrorMesage("Enter address");
        //     console.error('Invalid address');
            
        //     return ;
        // }
        // if(!isValidPhone(phone)){
        //     console.error('Invalid phone number');
        //     return;
        // }
            fetch("/create-checkout-session-M/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ address: address, phone: phone})
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

    function isValidAddress(address){

        //google map api street verfication
    
        return address.trim() !== '';
    }
    
    // function isValidPhone(phone){
    
    //     //add more phone verfication such as country code
    //     return /^\d{10}$/.test(phone);
    // }

    // function showErrorMesage(message){
    //     const errorMessage = document.getElementById('errorMessage');
    //     const errorText = document.getElementById('errorText');

    //     if(errorMessage && errorText){
    //         errorText.textContent = message;
    //         errorMessage.style.display = 'block';
    //     }
    // }