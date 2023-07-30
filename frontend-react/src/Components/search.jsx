import {React, Component } from 'react';
import axios from 'axios'

export default class Search extends Component {
    constructor(props) {
    super(props);
    this.state = {
        post: [],
    };
    console.log(props.location.state.query);
    this.query = props.location.state.query;
    // this.params = new URLSearchParams([['search',this.query],['page',1]]);
    // console.log(this.params);
    this.params = {
        params:{
        search: this.query,
        page: 1
    }}
    }
    componentDidMount(){
    axios.get('http://127.0.0.1:5000/api/search', this.params).then((response) => {
        console.log(response.data);
        this.setState({ post: response.data });
        console.log(this.state.post);
      }).catch(
        function (error) {
          console.log('Show error notification!')
          return Promise.reject(error)
        }
      );
    }


    render(){
        return (
            <div className="flex flex-col ml-96 my-32 justify-center text-left">
                <h1 className="text-5xl font-lg font-mono leading-tight text-blue-400">Results</h1>
                {/* <ol> */}
                    {this.state.post.map((x, index)=>{
                        return <div className="text-white my-4 text-xl" key={index}><a href={x[0]}>{x[0]}</a></div>
                    })}
                {/* </ol> */}
            </div>
        );
    } 

}

// export default withRouter(Search);


// export default function Search(){
//     const [post,setPost] = useState([]); 
//     const {
//       query: { search },
//     } = router
//     console.log(search)
//     const params = new URLSearchParams([['search',search],['page',1]]);

//     useEffect(()=> axios.get('http://127.0.0.1:5000/api/search',{ params }).then((response) => {
//         console.log(response.data)
//         setPost(response.data);
//         console.log(post);
//       }),[]);
//     return (
//         <div className="flex flex-col ml-96 my-32 justify-center text-left">
//             <h1 className="text-5xl font-lg font-mono leading-tight text-blue-400">Results</h1>
//             {/* <ol> */}
//                 {post.map((x, index)=>{
//                     return <div className="text-white my-4 text-xl" key={index}><a href={x[0]}>{x[0]}</a></div>
//                 })}
//             {/* </ol> */}
//         </div>
//     )
// };