import React, { useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [query, setQuery] = useState<string>("");

  function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    console.log((e.target as HTMLButtonElement).value);
    setQuery(e.target.value);
  }
  return (
    <div className="flex flex-col items-center justify-center mx-auto min-h-screen">
      <div className="">
        <h1 className="text-5xl font-lg font-mono leading-tight text-blue-400">
          Vision: The Search Engine
        </h1>
      </div>
      <form className="my-20 w-2/5 border-blue-900 flex flex-col justify-center items-center">
        <input
          className="border-4 border-blue-500 w-full px-7 py-3 shadow-sm focus:bg-gray-100 focus:border-blue-900 rounded-full mb-10"
          type="text"
          placeholder="Vision Search"
          onChange={(e) => onChange(e)}
        ></input>
        <div className="flex flex-row justify-around">
            <Link  className="bg-blue-300 w-1/3 px-4 py-3 text-xl text-gray-700 rounded-md hover:bg-blue-500 duration-500 hover:text-white"

              to={{ pathname: `/search`, state: { query: query } }} // add page number
            >
              Search Now!
            </Link>
          

          <Link
           className="bg-blue-300 w-1/3 px-4 py-3 text-xl text-gray-700 rounded-md hover:bg-blue-500 duration-500 hover:text-white"
          to = {{pathname: `/request/crawl`}}
          >
            Request Crawl
          </Link>
        </div>
        
      </form>
    </div>
  );
}

export default Home;
