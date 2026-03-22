const http = require('http');

const data = JSON.stringify({
    email: 'ejemplo5@gmail.com',
    password: 'password123'
});

const loginReq = http.request({
    hostname: '127.0.0.1',
    port: 8000,
    path: '/api/auth/login',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
}, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
        try {
            const token = JSON.parse(body).access_token;
            console.log('Got token:', token ? 'YES' : 'NO');
            if (!token) {
                console.log('Login failed:', body);
                return;
            }
            
            const statsReq = http.request({
                hostname: '127.0.0.1',
                port: 8000,
                path: '/api/user/stats',
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token
                }
            }, (res2) => {
                let body2 = '';
                res2.on('data', chunk => body2 += chunk);
                res2.on('end', () => console.log('Stats:', body2, 'Status:', res2.statusCode));
            });
            statsReq.end();
        } catch (e) {
            console.error(e, body);
        }
    });
});

loginReq.on('error', console.error);
loginReq.write(data);
loginReq.end();
