import axios from 'axios';
import {useState} from 'react';


function isUrlValid(str: string) {
    const pattern = new RegExp(
      '^(https?:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR IP (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
        '(\\#[-a-z\\d_]*)?$', // fragment locator
      'i'
    );
    return pattern.test(str);
   }


function RequestCrawl() {
    const [url, setURL] = useState<string>('');


    const changeURL = (e: React.ChangeEvent<HTMLInputElement>) => {
        setURL(e.target.value);
    }
    const submitURL = () => {
        console.log('submitting url');
        console.log(url);
        const params = {params: {url: url}};

        if (isUrlValid(url)) {
            console.log('url is valid');
            axios.get('http://localhost:8080/api/requestCrawl', params).then((res) => {
                console.log(res);
                console.log(res.data);
            })
        }
        else{
            console.log('url is invalid');
            alert('url is invalid');
            setURL('');
        }
    }


        return (
            <div>
                <h1>Request Crawl</h1>
                Make a request to crawl a website
                <input type="text" placeholder="Enter URL" value={url} onChange={changeURL}/>
                <button onClick={submitURL}>Submit request</button>
            </div>
        );
}


export default RequestCrawl;