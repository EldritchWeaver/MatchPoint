

/**
 * @file Módulo principal de la aplicación de consola para interactuar con la MatchPoint API.
 * @description Este archivo contiene la lógica para registrar usuarios, iniciar sesión, y gestionar equipos, torneos, partidos e inscripciones a través de una interfaz de línea de comandos (CLI).
 * @author Tu Nombre
 * @version 1.0.0
 */

const axios = require('axios');
const readline = require('readline');

// URL base de la API
const API_URL = 'http://localhost:8000';
// Almacena el token de autenticación JWT
let authToken = null;

// Crea una interfaz de lectura para la entrada y salida de la consola
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

/**
 * Envuelve la función `rl.question` en una promesa para poder usar `await`.
 * @param {string} query - La pregunta a mostrar al usuario.
 * @returns {Promise<string>} La respuesta del usuario.
 */
function question(query) {
    return new Promise(resolve => {
        rl.question(query, resolve);
    });
}

/**
 * Registra un nuevo usuario en el sistema.
 * Solicita nombre, nickname, email y contraseña.
 */
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

/**
 * Inicia sesión en la API y guarda el token JWT para futuras solicitudes.
 * Solicita email y contraseña.
 */
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

/**
 * Busca un usuario por su nickname y muestra la información.
 */
async function getUserByNickname() {
    const nickname = await question('Nickname del usuario a buscar: ');
    try {
        const response = await axios.get(`${API_URL}/users/nickname/${nickname}`);
        console.log('Usuario encontrado:', response.data);
    } catch (error) {
        console.error('Error buscando usuario:', error.response ? error.response.data : error.message);
    }
}

/**
 * Crea un nuevo equipo. Requiere que el usuario haya iniciado sesión.
 * Solicita el nombre del equipo y el ID del capitán.
 */
async function createTeam() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const nombre = await question('Nombre del equipo: ');
    const id_capitan = await question('ID del capitán: ');

    try {
        const { data: teams } = await axios.get(`${API_URL}/teams/`);
        const isCaptain = teams.some(team => team.id_capitan === parseInt(id_capitan));

        if (isCaptain) {
            console.error('Error: Este usuario ya es capitán de otro equipo.');
            return;
        }

        const response = await axios.post(`${API_URL}/teams/`, { nombre, id_capitan: parseInt(id_capitan) });
        console.log('Equipo creado:', response.data);
    } catch (error) {
        console.error('Error creando equipo:', error.response ? error.response.data : error.message);
    }
}

/**
 * Crea un nuevo torneo. Requiere que el usuario haya iniciado sesión.
 * Solicita toda la información necesaria para crear el torneo.
 */
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
    const estado = await question('Estado del torneo (programado, en_curso, finalizado): ');
    const stream_url = await question('URL del stream: ');
    const id_organizador = await question('ID del organizador: ');

    try {
        const response = await axios.post(`${API_URL}/tournaments/`, {
            nombre,
            descripcion,
            fecha_inicio,
            fecha_fin,
            max_equipos: parseInt(max_equipos),
            estado,
            stream_url,
            id_organizador: parseInt(id_organizador)
        });
        console.log('Torneo creado:', response.data);
    } catch (error) {
        console.error('Error creando torneo:', error.response ? error.response.data : error.message);
    }
}

/**
 * Lista todos los torneos que coinciden con un estado específico.
 */
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

/**
 * Inscribe un equipo en un torneo. Requiere que el usuario haya iniciado sesión.
 */
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

/**
 * Registra un pago para la inscripción de un equipo en un torneo. Requiere que el usuario haya iniciado sesión.
 */
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

/**
 * Crea un nuevo partido en un torneo. Requiere que el usuario haya iniciado sesión.
 */
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

/**
 * Obtiene y muestra una lista completa de todas las entidades de la API.
 */
async function listAll() {
    try {
        const [users, teams, tournaments, inscriptions, payments, matches, members] = await Promise.all([
            axios.get(`${API_URL}/users/`),
            axios.get(`${API_URL}/teams/`),
            axios.get(`${API_URL}/tournaments/`),
            axios.get(`${API_URL}/inscriptions/`),
            axios.get(`${API_URL}/payments/`),
            axios.get(`${API_URL}/matches/`),
            axios.get(`${API_URL}/members/`)
        ]);

        console.log('\n--- Usuarios ---');
        console.table(users.data);
        console.log('\n--- Equipos ---');
        console.table(teams.data);
        console.log('\n--- Miembros de Equipo ---');
        console.table(members.data);
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

/**
 * Agrega un miembro a un equipo con un rol específico. Requiere que el usuario haya iniciado sesión.
 */
async function addTeamMember() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }
    const id_equipo = await question('ID del equipo: ');
    const id_usuario = await question('ID del usuario a agregar: ');
    const rol = await question('Rol del nuevo miembro (jugador, capitan, suplente): ');

    try {
        const response = await axios.post(`${API_URL}/members/`, { 
            id_equipo: parseInt(id_equipo), 
            id_usuario: parseInt(id_usuario),
            rol
        });
        console.log('Miembro agregado al equipo:', response.data);
    } catch (error) {
        console.error('Error agregando miembro:', error.response ? error.response.data : error.message);
    }
}

/**
 * Muestra los miembros de un equipo específico.
 */
async function viewTeamMembers() {
    const teamId = await question('Introduce el ID del equipo para ver sus miembros: ');
    if (!teamId || isNaN(parseInt(teamId))) {
        console.log('ID de equipo no válido.');
        return;
    }

    try {
        const { data: members } = await axios.get(`${API_URL}/members/`);
        const teamMembers = members.filter(member => member.id_equipo === parseInt(teamId));

        if (teamMembers.length === 0) {
            console.log('No se encontraron miembros para este equipo o el equipo no existe.');
            return;
        }

        console.log(`\n--- Miembros del Equipo ID: ${teamId} ---`);
        console.table(teamMembers);
    } catch (error) {
        console.error('Error al obtener los miembros del equipo:', error.response ? error.response.data : error.message);
    }
}

/**
 * Actualiza el resultado de un partido. Requiere que el usuario haya iniciado sesión.
 */
async function updateMatchResult() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }

    const matchId = await question('ID del partido a actualizar: ');
    const resultado_local = await question('Resultado del equipo local: ');
    const resultado_visitante = await question('Resultado del equipo visitante: ');

    if (!matchId || isNaN(parseInt(matchId)) || isNaN(parseInt(resultado_local)) || isNaN(parseInt(resultado_visitante))) {
        console.log('Datos no válidos. Asegúrate de que los IDs y resultados sean números.');
        return;
    }

    try {
        const response = await axios.put(`${API_URL}/matches/${matchId}`, {
            resultado_local: parseInt(resultado_local),
            resultado_visitante: parseInt(resultado_visitante)
        });
        console.log('Resultado del partido actualizado:', response.data);
    } catch (error) {
        console.error('Error actualizando el resultado:', error.response ? error.response.data : error.message);
    }
}

/**
 * Actualiza el estado de un torneo. Requiere que el usuario haya iniciado sesión.
 */
async function updateTournamentStatus() {
    if (!authToken) {
        console.log('Debes iniciar sesión primero.');
        return;
    }

    const tournamentId = await question('ID del torneo a actualizar: ');
    const status = await question('Nuevo estado (programado, en_curso, finalizado): ');

    if (!tournamentId || isNaN(parseInt(tournamentId))) {
        console.log('ID de torneo no válido.');
        return;
    }

    try {
        const response = await axios.put(`${API_URL}/tournaments/${tournamentId}/status`, { status });
        console.log('Estado del torneo actualizado:', response.data);
    } catch (error) {
        console.error('Error actualizando el estado del torneo:', error.response ? error.response.data : error.message);
    }
}

/**
 * Muestra el menú de gestión de usuarios y maneja la selección del usuario.
 */
async function userMenu() {
    console.log('\n--- Gestión de Usuarios y Sesión ---');
    console.log('1. Registrar nuevo usuario');
    console.log('2. Iniciar sesión');
    console.log('3. Buscar usuario por nickname');
    console.log('4. Volver al menú principal');

    const choice = await question('Elige una opción: ');
    switch (choice) {
        case '1': await registerUser(); break;
        case '2': await login(); break;
        case '3': await getUserByNickname(); break;
        case '4': return;
        default: console.log('Opción no válida.');
    }
}

/**
 * Muestra el menú de gestión de equipos y maneja la selección del usuario.
 */
async function teamMenu() {
    if (!authToken) {
        console.log('Debes iniciar sesión para gestionar equipos.');
        return;
    }
    console.log('\n--- Gestión de Equipos ---');
    console.log('1. Crear equipo');
    console.log('2. Agregar miembro a equipo');
    console.log('3. Ver miembros de un equipo');
    console.log('4. Volver al menú principal');

    const choice = await question('Elige una opción: ');
    switch (choice) {
        case '1': await createTeam(); break;
        case '2': await addTeamMember(); break;
        case '3': await viewTeamMembers(); break;
        case '4': return;
        default: console.log('Opción no válida.');
    }
}

/**
 * Muestra el menú de gestión de torneos y maneja la selección del usuario.
 */
async function tournamentMenu() {
    if (!authToken) {
        console.log('Debes iniciar sesión para gestionar torneos.');
        return;
    }
    console.log('\n--- Gestión de Torneos ---');
    console.log('1. Crear torneo');
    console.log('2. Listar torneos por estado');
    console.log('3. Inscribir equipo a torneo');
    console.log('4. Registrar pago de inscripción');
    console.log('5. Crear partido');
    console.log('6. Actualizar resultado de un partido');
    console.log('7. Actualizar estado de un torneo');
    console.log('8. Volver al menú principal');

    const choice = await question('Elige una opción: ');
    switch (choice) {
        case '1': await createTournament(); break;
        case '2': await listTournamentsByStatus(); break;
        case '3': await createInscription(); break;
        case '4': await createPayment(); break;
        case '5': await createMatch(); break;
        case '6': await updateMatchResult(); break;
        case '7': await updateTournamentStatus(); break;
        case '8': return;
        default: console.log('Opción no válida.');
    }
}

/**
 * Muestra el menú principal de la aplicación y maneja la navegación.
 */
async function mainMenu() {
    while (true) {
        console.log('\n--- Menú Principal ---');
        console.log('1. Gestión de Usuarios y Sesión');
        console.log('2. Gestión de Equipos');
        console.log('3. Gestión de Torneos');
        console.log('4. Ver todo');
        console.log('5. Salir');

        const choice = await question('Elige una sección: ');

        switch (choice) {
            case '1': await userMenu(); break;
            case '2': await teamMenu(); break;
            case '3': await tournamentMenu(); break;
            case '4': await listAll(); break;
            case '5': rl.close(); return;
            default: console.log('Opción no válida.');
        }
    }
}

// Inicia la aplicación
mainMenu();

