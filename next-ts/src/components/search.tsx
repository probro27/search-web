import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom';
import axios from 'axios'

interface LocationState {
  pathname: string;
  state: {
    query: string;
    // add page number
  };
}

interface Results {
  data: Array<Array<string | number>> | undefined;
}

function Search() {
  const location: LocationState = useLocation();
  const forceUpdate = React.useReducer(() => ({}), {})[1] as () => void;
  const [results,] = useState<Results>({data: undefined});
  const API_URL = 'http://127.0.0.1:8080/api/search';
  console.log(location.state.query);
  const params = {params: {search: location.state.query, page: 1}};

  useEffect(() => {
      axios.get(API_URL, params).then((response) => {
          console.log(response.data);
          results.data =  response.data as Array<Array<string| number>>;
          console.log(results);
          forceUpdate();
      });
  }, []);

  return (
      <div className="flex flex-col ml-96 my-32 justify-center text-left">
          <h1 className="text-5xl font-lg font-mono leading-tight text-blue-400">Results</h1>
              {results.data?.map((x, index)=>{
                  return <div className="text-white my-4 text-xl" key={index}><a href={(x[0] as string)}>{x[0]}</a></div>
              })}
      </div>
  )
}

export default Search;
