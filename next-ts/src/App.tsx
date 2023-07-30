import "./App.css";
import {
BrowserRouter as Router,
Switch,
Route,
Redirect,
} from "react-router-dom";

// import Home component
import Home from "./components/home";
// import About component
import Search from "./components/search";
// import ContactUs component
import RequestCrawl from "./components/requestCrawl";
function App() {
return (
	<>
	{/* This is the alias of BrowserRouter i.e. Router */}
	<Router forceRefresh={true}>
		<Switch>
		{/* This route is for home component
		with exact path "/", in component props
		we passes the imported component*/}
		<Route exact path="/" component={Home} />
			
		{/* This route is for about component
		with exact path "/about", in component
		props we passes the imported component*/}
		<Route path="/search" component={Search} />

		{/* This route is for contactus component
		with exact path "/contactus", in
		component props we passes the imported component*/}
		<Route path="/request/crawl" component={RequestCrawl} />
			
		{/* If any route mismatches the upper
		route endpoints then, redirect triggers
		and redirects app to home component with to="/" */}
		<Redirect to="/" />
		</Switch>
	</Router>
	</>
);
}

export default App;
