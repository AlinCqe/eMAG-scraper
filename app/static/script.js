

document.getElementById('scrapeForm').addEventListener('submit', function(e){
    e.preventDefault();

    const search_item = document.getElementById('item').value;
    const deepSearch = document.getElementById("deepSearch").checked;


    fetch('/htmlscraper', 
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query: search_item})
        }
    )
    .then(response => response.json())
    .then(data => {console.log(data);
    console.log(deepSearch)   
        return fetch('/firstapiscraper')
        
    .then(response => response.json())
    .then(data => {console.log(data)

        if (deepSearch){

            return fetch('/secondapiscraper')

        .then(response => response.json())
        .then(data => {console.log(data)})
        }

        })
    })
})