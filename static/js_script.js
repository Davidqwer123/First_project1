console.log('Я працюю');
const routes = [
    { path: '/sign_up_pg', handler: signupHandler },
    { path: '/login_pg', handler: loginHandler },
    { path: '/see_pg', handler: seeHandler },
    { path: '/weather_pg', handler: weatherHandler },
    { path: '/translate_pg', handler: translateHandler }


];

function RequestToServer(form, url) {
    const formData = new FormData(form);
    console.log('Я RequestToServer');
    formData.append('key1', 'value1');

    return new Promise((resolve, reject) => {
        fetch(url, {
            method: "POST",
            body: formData,

        })
        .then(response => response.json())
        .then(data => {
            resolve(data);
        });
    });
}

function signupHandler() {
    const Form = document.querySelector('#signup-form');
    const res = document.getElementById('result');
    const urlSignup = '/signup';
    console.log('Я signupHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlSignup)
        .then(response => {
        res.innerHTML = `<p>${response.message}</p>`});
    });
};

function seeHandler() {
    const Form = document.querySelector('#see-form');
    const res = document.getElementById('result');
    const urlSignup = '/see_text';
    console.log('Я signupHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlSignup)
        .then(response => {
        res.innerHTML = ``;
        const text = response['data'];
            text.forEach(event => {
            res.innerHTML +=`
            <p>Перший запис:${event['info1']}</p>
            <p>Другий запис:${event['info2']}</p>`;
                });
            });
    });
};

function textHandler() {
    const Form = document.querySelector('#text-form');
    const res = document.getElementById('result');
    const urlText = '/text';
    console.log('Я signupHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlText)
        .then(response => {
        res.innerHTML = `<p>${response.message}</p>`});
    });
};

function loginHandler() {
    const Form = document.querySelector('#login-form');
    const res = document.getElementById('result');

    const urlLogin = '/login';
    console.log('Я loginHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlLogin)
        .then(response => {
            res.innerHTML = `<p>${response.message}</p>`;
        });
    });
};

function translateHandler() {
    const Form = document.querySelector('#test-form');
    const res = document.getElementById('result');

    const urlLogin = '/test_route';
    console.log('Я loginHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlLogin)
        .then(response => {
            res.innerHTML = `<p>${response.res}</p>`;
        });
    });
};

function handleRoutes() {
    const currentPath = window.location.pathname;
    console.log('Я  handleRoutes');
    const routeData = routes.find(route => route.path === currentPath);
    routeData.handler();
};

function weatherHandler() {
    const Form = document.querySelector('#wth-form');
    const res = document.getElementById('result');

    const urlWeather = '/weather';
    console.log('Я loginHandler');
    Form.addEventListener('submit', (event) => {
        event.preventDefault();
        RequestToServer(event.target, urlWeather)
        .then(response => {
            res.innerHTML = `<p>Тeмпература: ${response["Тeмпература"]}°</p> <p>Вологість: ${response["Вологість"]} %</p> <p> Швидкість вітру: ${response["Швидкість вітру:"]} км/год</p>`;
        });
    });
};

document.addEventListener("DOMContentLoaded", function() {
    handleRoutes();
});
