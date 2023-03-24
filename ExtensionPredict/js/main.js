
const processAddress = (address) => {
    const addressList = address.split(",")?.map(item => item.trim()).reverse();
    return { ward: addressList[2], district: addressList[1], city: addressList[0] }
}
const processString = (stringText) => {
    const listString = stringText.split(" ")
    return listString[0]
}
const returnDataFromBE = (data) => {
    const endpointAddress = 'http://127.0.0.1:8000/home/';

    // fetch(endpointAddress, {
    //     method: 'GET',

    // }).then((response) => {
    //     console.log("response", response);
    // }).then(dataReturn => {
    //     console.log("dataReturn", dataReturn);

    // }).catch(error => {

    //     console.log("error", error);
    // })
    // return;



    fetch(endpointAddress, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
        // body: JSON.stringify({
        //     ward: data['ward'],
        //     district: data['district'],
        //     city: data['city'],
        //     price: data['price'],
        //     square: data['square'],
        //     year: data['year']
        // })
    })
        .then(response => {

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(dataReturn => {
            const price = parseInt(dataReturn);
            console.log('text:', dataReturn.text);
            const formattedPrice = price.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' });
            const gia_de_xuat = `<div class = "show_price_predict"><div class="hien_thi_gia">Giá đề xuất : ${formattedPrice}</div></div>`;
            const wraperObject = document.querySelector('#product-detail-web > div.re__section.re__pr-description.js__section');
            if (wraperObject != null) {
                wraperObject.insertAdjacentHTML("beforebegin", gia_de_xuat);
            }
            console.log('Success:', dataReturn);
        })
        .catch(error => {
            console.error('Error:', error);
        })



}
const crawlData = () => {
    const currentPrice = document.querySelector("#product-detail-web > div.re__pr-short-info.js__pr-short-info > div:nth-child(1) > span.value").innerHTML;
    const currentSquare = document.querySelector("#product-detail-web > div.re__pr-short-info.js__pr-short-info > div:nth-child(2) > span.value").innerHTML;
    const address = document.querySelector("#product-detail-web > span").innerHTML;
    const date = document.querySelector("#product-detail-web > span").innerHTML;
    const { ward, district, city } = processAddress(address);
    const price = processString(currentPrice);
    const square = processString(currentSquare);
    const year = date.split('/')[2]
    return { ward, district, city, price, square, year }
}
const main = async () => {
    const data = crawlData()
    returnDataFromBE(data)
}

main();