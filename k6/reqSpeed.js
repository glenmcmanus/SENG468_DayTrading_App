import http from 'k6/http';

export default function () {
	const headers = { 'Content-Type': 'application/json' };
  const res = http.put('http://localhost:5101/add', {'userID':'asf','value':'10.00'}, { headers: headers });
 console.log(res.body) 
}
