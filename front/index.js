

const axios = require('axios');
const readline = require('readline');

const API_URL = 'http://localhost:8000';
let authToken = null;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function question(query) {
    return new Promise(resolve => {
        rl.question(query, resolve);
    });
}

async function registerUser() {
    const nombre = await question('Nombre: ');
    const nickname = await question('Nickname: ');
    const email = await question('Email: ');
    const password = await question('Password: ');

    try {
        const response = await axios.post(`${API_URL}/users/`, {
            nombre,
            nickname,
            email,
            pwd_hash: password
        });
        console.log('Usuario registrado:', response.data);
    } catch (error) {
        console.error('Error registrando usuario:', error.response ? error.response.data : error.message);
    }
}

async function login() {
    const email = await question('Email: ');
    const password = await question('Password: ');

    try {
        const response = await axios.post(`${API_URL}/users/token`, new URLSearchParams({
            username: email,
            password: password
        }));
        authToken = response.data.access_token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
        console.log('Login exitoso. Token guardado.');
    } catch (error) {
        console.error('Error en el login:', error.response ? error.response.data : error.message);
    }
}

async function getUserByNickname() {
    const nickname = await question('Nickname del usuario a buscar: ');
    try {
        const response = await axios.get(`${API_URL}/users/nickname/${nickname}`);
        console.log('Usuario encontrado:', response.data);
    } catch (error) {
        console.error('Error buscando usuario:', error.response ? error.response.data : error.message);
    }
}

async function createTeam() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const nombre = await question('Nombre del equipo: ');
    const id_capitan = await question('ID del capitán: ');

    try {
        const response = await axios.post(`${API_URL}/teams/`, { nombre, id_capitan: parseInt(id_capitan) });
        console.log('Equipo creado:', response.data);
    } catch (error) {
        console.error('Error creando equipo:', error.response ? error.response.data : error.message);
    }
}


async function createTournament() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const nombre = await question('Nombre del torneo: ');
    const descripcion = await question('Descripción: ');
    const fecha_inicio = await question('Fecha de inicio (YYYY-MM-DDTHH:MM:SSZ): ');
    const fecha_fin = await question('Fecha de fin (YYYY-MM-DDTHH:MM:SSZ): ');
    const max_equipos = await question('Máximo de equipos: ');
    const stream_url = await question('URL del stream: ');
    const id_organizador = await question('ID del organizador: ');

    try {
        const response = await axios.post(`${API_URL}/tournaments/`, {
            nombre,
            descripcion,
            fecha_inicio,
            fecha_fin,
            max_equipos: parseInt(max_equipos),
            stream_url,
            id_organizador: parseInt(id_organizador)
        });
        console.log('Torneo creado:', response.data);
    } catch (error) {
        console.error('Error creando torneo:', error.response ? error.response.data : error.message);
    }
}

async function listTournamentsByStatus() {
    const status = await question('Estado del torneo (programado, en_curso, finalizado): ');
    try {
        const response = await axios.get(`${API_URL}/tournaments/status/${status}`);
        console.log(`Torneos con estado '${status}':`);
        console.table(response.data);
    } catch (error) {
        console.error('Error listando torneos:', error.response ? error.response.data : error.message);
    }
}

async function createInscription() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const id_equipo = await question('ID del equipo: ');
    const id_torneo = await question('ID del torneo: ');

    try {
        const response = await axios.post(`${API_URL}/inscriptions/`, { id_equipo: parseInt(id_equipo), id_torneo: parseInt(id_torneo) });
        console.log('Inscripción creada:', response.data);
    } catch (error) {
        console.error('Error creando inscripción:', error.response ? error.response.data : error.message);
    }
}

async function createPayment() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const id_equipo = await question('ID del equipo: ');
    const id_torneo = await question('ID del torneo: ');
    const monto_cent = await question('Monto en centavos: ');

    try {
        const response = await axios.post(`${API_URL}/payments/`, { 
            id_equipo: parseInt(id_equipo), 
            id_torneo: parseInt(id_torneo),
            monto_cent: parseInt(monto_cent)
        });
        console.log('Pago registrado:', response.data);
    } catch (error) {
        console.error('Error registrando pago:', error.response ? error.response.data : error.message);
    }
}

async function createMatch() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const id_torneo = await question('ID del torneo: ');
    const equipo_local = await question('ID del equipo local: ');
    const equipo_visitante = await question('ID del equipo visitante: ');
    const fecha = await question('Fecha (YYYY-MM-DDTHH:MM:SSZ): ');

    try {
        const response = await axios.post(`${API_URL}/matches/`, { 
            id_torneo: parseInt(id_torneo), 
            equipo_local: parseInt(equipo_local), 
            equipo_visitante: parseInt(equipo_visitante), 
            fecha 
        });
        console.log('Partido creado:', response.data);
    } catch (error) {
        console.error('Error creando partido:', error.response ? error.response.data : error.message);
    }
}

async function listAll() {
    try {
        const [users, teams, tournaments, inscriptions, payments, matches] = await Promise.all([
            axios.get(`${API_URL}/users/`),
            axios.get(`${API_URL}/teams/`),
            axios.get(`${API_URL}/tournaments/`),
            axios.get(`${API_URL}/inscriptions/`),
            axios.get(`${API_URL}/payments/`),
            axios.get(`${API_URL}/matches/`)
        ]);

        console.log('\n--- Usuarios ---');
        console.table(users.data);
        console.log('\n--- Equipos ---');
        console.table(teams.data);
        console.log('\n--- Torneos ---');
        console.table(tournaments.data);
        console.log('\n--- Inscripciones ---');
        console.table(inscriptions.data);
        console.log('\n--- Pagos ---');
        console.table(payments.data);
        console.log('\n--- Partidos ---');
        console.table(matches.data);

    } catch (error) {
        console.error('Error listando todo:', error.response ? error.response.data : error.message);
    }
}

async function mainMenu() {
    while (true) {
        console.log('\n--- Menú Principal ---');
        console.log('1. Registrar usuario');
        console.log('2. Iniciar sesión');
        console.log('3. Buscar usuario por nickname');
        console.log('4. Crear equipo');
        console.log('5. Crear torneo');
        console.log('6. Listar torneos por estado');
        console.log('7. Inscribir equipo a torneo');
        console.log('8. Registrar pago de inscripción');
        console.log('9. Crear partido');
        console.log('10. Listar todo');
        console.log('11. Salir');

        const choice = await question('Elige una opción: ');

        switch (choice) {
            case '1':
                await registerUser();
                break;
            case '2':
                await login();
                break;
            case '3':
                await getUserByNickname();
                break;
            case '4':
                await createTeam();
                break;
            case '5':
                await createTournament();
                break;
            case '6':
                await listTournamentsByStatus();
                break;
            case '7':
                await createInscription();
                break;
            case '8':
                await createPayment();
                break;
            case '9':
                await createMatch();
                break;
            case '10':
                await listAll();
                break;
            case '11':
                rl.close();
                return;
            default:
                console.log('Opción no válida.');
        }
    }
}

mainMenu();

