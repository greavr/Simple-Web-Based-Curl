const form = document.querySelector("#curl_form");

async function do_curl(){
    // Capture the latest form info:
    const formData = new FormData(form);
    // Disable post button
    document.getElementById("Submit").disabled = true;

    // Attempt the curl
    try {
        target_url += formData;
        fetch( '/curl', {
            method: 'POST',
            body: formData
          })
        .then( response => response.json() )
        .then( response => {
            // Do something with response.
            $('#curl_result').append("~~~~~~~~~~~~~");
            let Newheader = "> " + formData.get("target_url")
            $('#curl_result').append(Newheader);
        } );
    } catch (e) {
        console.error(e);
    }    

    document.getElementById("Submit").disabled = false;
}