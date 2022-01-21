import React from 'react'; 
import axios from "axios";
import { useState, useEffect } from 'react';
import Search from './Search';
import SearchItem from './SearchItem';


function Results({search,query,setQuery}) {

    const [post,setPost] = useState([]); 

    const params = new URLSearchParams([['search',search],['page',1]]);

    useEffect(()=> axios.get('http://127.0.0.1:5000/api/search',{ params }).then((response) => {
        setPost(response.data);
      }),[]);


    return (
        <div>
            <Search 
            query = {query}
            setQuery = {setQuery}
            />
            {console.log(search)}
            {console.log(post)}
            <ol>
                {post.map((x)=>{
                    return <div><li><a href={x[0]}>{x[2]}</a></li></div>
                })}
            </ol>
        </div>
    )
}

export default Results

