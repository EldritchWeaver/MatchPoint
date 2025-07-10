import axios from 'axios';

const API_URL = 'http://192.168.1.108:8000'; // Asegúrate de que esta IP sea la correcta y accesible

export function setAuthToken(token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export async function registerUser({ nombre, nickname, email, password }) {
    return axios.post(`${API_URL}/users/`, { nombre, nickname, email, password });
}

export async function login({ email, password }) {
    return axios.post(`${API_URL}/users/token`, new URLSearchParams({ username: email, password }));
}

export async function getUserByNickname(nickname) {
    return axios.get(`${API_URL}/users/nickname/${nickname}`);
}

export async function createTeam({ nombre, id_capitan }) {
    return axios.post(`${API_URL}/teams/`, { nombre, id_capitan: parseInt(id_capitan) });
}

export async function createTournament(data) {
    return axios.post(`${API_URL}/tournaments/`, {
        ...data,
        max_equipos: parseInt(data.max_equipos),
        id_organizador: parseInt(data.id_organizador)
    });
}

export async function listTournamentsByStatus(status) {
    return axios.get(`${API_URL}/tournaments/status/${status}`);
}

export async function createInscription({ id_equipo, id_torneo }) {
    return axios.post(`${API_URL}/inscriptions/`, { id_equipo: parseInt(id_equipo), id_torneo: parseInt(id_torneo) });
}

export async function createPayment({ id_equipo, id_torneo, monto_cent }) {
    return axios.post(`${API_URL}/payments/`, { id_equipo: parseInt(id_equipo), id_torneo: parseInt(id_torneo), monto_cent: parseInt(monto_cent) });
}

export async function createMatch({ id_torneo, equipo_local, equipo_visitante, fecha }) {
    return axios.post(`${API_URL}/matches/`, { id_torneo: parseInt(id_torneo), equipo_local: parseInt(equipo_local), equipo_visitante: parseInt(equipo_visitante), fecha });
}

export async function listAll() {
    return Promise.all([
        axios.get(`${API_URL}/users/`),
        axios.get(`${API_URL}/teams/`),
        axios.get(`${API_URL}/tournaments/`),
        axios.get(`${API_URL}/inscriptions/`),
        axios.get(`${API_URL}/payments/`),
        axios.get(`${API_URL}/matches/`),
        axios.get(`${API_URL}/members/`)
    ]);
}

export async function addTeamMember({ id_equipo, id_usuario, rol }) {
    return axios.post(`${API_URL}/members/`, { id_equipo: parseInt(id_equipo), id_usuario: parseInt(id_usuario), rol });
}

export async function getAllMembers() {
    return axios.get(`${API_URL}/members/`);
}

export async function updateMatchResult({ matchId, resultado_local, resultado_visitante }) {
    return axios.put(`${API_URL}/matches/${matchId}`, {
        resultado_local: parseInt(resultado_local),
        resultado_visitante: parseInt(resultado_visitante)
    });
}

export async function updateTournamentStatus({ tournamentId, status }) {
    return axios.put(`${API_URL}/tournaments/${tournamentId}/status`, { status });
}
