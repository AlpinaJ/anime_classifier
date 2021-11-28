document.querySelector("#file").addEventListener("change", function () {
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        localStorage.setItem("recent-image", reader.result);
    });
    reader.readAsDataURL(this.files[0]);
});
document.querySelector("#button").addEventListener("click", function () {
    window.location.reload();
});

let label_html = document.querySelector("#result");

document.addEventListener("DOMContentLoaded", () => {
    const recentImage = localStorage.getItem("recent-image");
    if (recentImage) {
        document.querySelector("#image").setAttribute("src", recentImage);
    }

    console.log("request started")

    // convert base64 picture to blob
    function convertBase64ToBlob(base64Image) {
        // Split into two parts
        const parts = base64Image.split(';base64,');

        // Hold the content type
        const imageType = parts[0].split(':')[1];

        // Decode Base64 string
        const decodedData = window.atob(parts[1]);

        // Create UNIT8ARRAY of size same as row data length
        const uInt8Array = new Uint8Array(decodedData.length);

        // Insert all character code into uInt8Array
        for (let i = 0; i < decodedData.length; ++i) {
            uInt8Array[i] = decodedData.charCodeAt(i);
        }

        // Return BLOB image after conversion
        return new Blob([uInt8Array], {type: imageType});
    }

    let blob = convertBase64ToBlob(recentImage)

    let formData = new FormData();
    formData.set("image", blob, "test.png");

    let response = fetch("/classify", {
        method: 'POST',
        body: formData
    }).then(
        (result) => {
            result.json().then(
                (json_result) => {
                    console.log(json_result);
                    let label = json_result["label"];
                    console.log(label);
                    label_html.textContent = label;
                }
            )

        },
        () => {
            console.log("--------- CLASSIFY request failed")
        })
})