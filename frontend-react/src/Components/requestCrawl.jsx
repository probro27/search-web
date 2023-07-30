import {Component} from 'react';


function isUrlValid(str) {
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


export default class RequestCrawl extends Component {
    state = {
        url: ''
    }

    changeURL = (e) => {
        this.setState({url: e.target.value});
    }
    submitURL = () => {
        console.log('submitting url');
        console.log(this.state.url);
        if (isUrlValid(this.state.url)) {
            console.log('url is valid');
        }
        else{
            console.log('url is invalid');
            alert('url is invalid');
            this.setState({url: ''})
        }
    }


    render() {
        return (
            <div>
                <h1>Request Crawl</h1>
                Make a request to crawl a website
                <input type="text" placeholder="Enter URL" value={this.state.url} onChange={this.changeURL}/>
                <button onClick={this.submitURL}>Submit request</button>
            </div>
        );
    }
}
