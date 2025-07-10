import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator, RefreshControl, Image, TouchableOpacity, TextInput, Alert } from 'react-native'; // <-- TextInput añadido aquí
import { LinearGradient } from 'expo-linear-gradient';
import * as api from '../../api/index'; // Asegúrate de que esta ruta sea correcta
import { Picker } from '@react-native-picker/picker'; // Instala con: npm install @react-native-picker/picker

// Componente para mostrar un item de torneo en la lista
const TournamentItem = ({ tournament }) => {
  // Función para formatear la fecha y hora
  const formatDateTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <LinearGradient
      colors={['#1a2a3a', '#2c5364']} // Colores del gradiente para cada tarjeta de torneo
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.tournamentCard}
    >
      <View style={styles.cardHeader}>
        <Text style={styles.tournamentName}>{tournament.nombre}</Text>
        <Text style={styles.tournamentStatus}>Estado: {tournament.estado}</Text>
      </View>
      <Text style={styles.tournamentDescription}>{tournament.descripcion || 'Sin descripción.'}</Text>
      <View style={styles.cardDetails}>
        <Text style={styles.detailText}>Inicio: {formatDateTime(tournament.fecha_inicio)}</Text>
        <Text style={styles.detailText}>Fin: {formatDateTime(tournament.fecha_fin)}</Text>
        <Text style={styles.detailText}>Equipos Máx: {tournament.max_equipos}</Text>
        {tournament.stream_url && (
          <Text style={styles.detailText}>Stream: <Text style={styles.streamLink}>{tournament.stream_url}</Text></Text>
        )}
      </View>
      {/* Puedes añadir botones de acción aquí, como "Inscribirse" o "Ver Detalles" */}
      <TouchableOpacity style={styles.detailsButton}>
        <Text style={styles.detailsButtonText}>Ver Detalles</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
};

export default function HomeScreen({ navigation }) {
  const [tournaments, setTournaments] = useState([]); // Estado para almacenar la lista de torneos
  const [loading, setLoading] = useState(true); // Estado para el indicador de carga inicial
  const [refreshing, setRefreshing] = useState(false); // Estado para el "pull-to-refresh"
  const [error, setError] = useState(null); // Estado para manejar errores
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchVisible, setSearchVisible] = useState(false);
const [searchText, setSearchText] = useState('');



//filtro de torneos
const filteredTournaments = tournaments.filter(t =>
  t.nombre.toLowerCase().includes(searchText.toLowerCase()) ||
  (t.descripcion && t.descripcion.toLowerCase().includes(searchText.toLowerCase()))
);



  /**
   * Función para cargar los torneos desde la API.
   * Utiliza useCallback para memorizar la función y evitar re-creaciones innecesarias.
   */
  const fetchTournaments = useCallback(async () => {
  setError(null);
  try {
    const response = await api.listTournamentsByStatus('programado', selectedCategory); // Ajusta según tu API
    setTournaments(response.data);
  } catch (err) {
    setError('No se pudieron cargar los torneos. Verifica la conexión o la API.');
  } finally {
    setLoading(false);
    setRefreshing(false);
  }
}, [selectedCategory]);

  // useEffect para cargar los torneos cuando el componente se monta
  useEffect(() => {
    fetchTournaments();
  }, [fetchTournaments]); // Se ejecuta cuando fetchTournaments cambia (que es solo una vez)

  // Función para manejar el "pull-to-refresh"
  const onRefresh = useCallback(() => {
    setRefreshing(true); // Activa el indicador de refresco
    fetchTournaments(); // Vuelve a cargar los torneos
  }, [fetchTournaments]);

  // Si está cargando inicialmente, muestra un indicador
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#1e90ff" />
        <Text style={styles.loadingText}>Cargando torneos...</Text>
      </View>
    );
  }

  // Si hay un error y no hay torneos, muestra el mensaje de error
  if (error && tournaments.length === 0) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity onPress={fetchTournaments} style={styles.retryButton}>
          <Text style={styles.retryButtonText}>Reintentar</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <LinearGradient
      colors={['#0f2027', '#2c5364', '#203A43']} // Fondo de gradiente para toda la pantalla
      style={styles.container}
    >
      {/* Encabezado de la pantalla */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('Profile')}>
  <Text style={styles.headerIcon}>☰</Text>

        </TouchableOpacity>
        <TouchableOpacity onPress={() => setSearchVisible(!searchVisible)}>
  <Text style={styles.headerIcon}>🔍</Text>
</TouchableOpacity>

      </View>
{searchVisible && (
  <View style={{ paddingHorizontal: 20, paddingBottom: 10 }}>
    <TextInput
      style={{
        backgroundColor: 'rgba(255,255,255,0.15)',
        color: '#fff',
        borderRadius: 8,
        paddingHorizontal: 12,
        paddingVertical: 8,
        fontSize: 16,
      }}
      placeholder="Buscar torneo..."
      placeholderTextColor="#ccc"
      value={searchText}
      onChangeText={setSearchText}
      autoFocus
    />
  </View>
)}

<View style={styles.categoryFilter}>
  <Text style={styles.categoryText}>Categoría:</Text>
  <View style={styles.categoryDropdown}>
    <Picker
      selectedValue={selectedCategory}
      style={{ flex: 1, color: '#fff', backgroundColor: 'transparent' }}
      dropdownIconColor="#fff"
      onValueChange={(itemValue) => setSelectedCategory(itemValue)}
    >
      <Picker.Item label="Todas" value="" />
      <Picker.Item label="Fútbol" value="futbol" />
      <Picker.Item label="Básquet" value="basquet" />
      {/* Agrega más categorías según tu API */}
    </Picker>
  </View>
</View>

      {/* Lista de torneos */}
      {tournaments.length > 0 ? (
        <FlatList
  data={filteredTournaments}
  keyExtractor={(item) => item.id.toString()}
  renderItem={({ item }) => <TournamentItem tournament={item} />}
  contentContainerStyle={styles.listContentContainer}
  refreshControl={
    <RefreshControl
      refreshing={refreshing}
      onRefresh={onRefresh}
      tintColor="#fff"
    />
  }
/>
      
      ) : (
        // Mensaje si no hay torneos
        <View style={styles.noTournamentsContainer}>
          <Text style={styles.noTournamentsText}>No hay torneos disponibles en este momento.</Text>
          <TouchableOpacity onPress={fetchTournaments} style={styles.retryButton}>
            <Text style={styles.retryButtonText}>Recargar Torneos</Text>
          </TouchableOpacity>
          
        </View>
      )}

      {/* Barra de navegación inferior (basada en la segunda imagen) */}
   <View style={styles.bottomNavBar}>
  <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('Home')}>
    <Text style={styles.navIcon}>🏠</Text>
    <Text style={styles.navText}>Inicio</Text>
  </TouchableOpacity>
  <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('Explore')}>
    <Text style={styles.navIcon}>🧭</Text>
    <Text style={styles.navText}>Explorar</Text>
  </TouchableOpacity>
  <TouchableOpacity style={styles.navPlusButton} onPress={() => navigation.navigate('Create')}>
    <Text style={styles.navPlusIcon}>+</Text>
  </TouchableOpacity>
  <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('Chat')}>
    <Text style={styles.navIcon}>💬</Text>
    <Text style={styles.navText}>Chat</Text>
  </TouchableOpacity>
  <TouchableOpacity style={styles.navItem} onPress={() => navigation.navigate('Profile')}>
    <Text style={styles.navIcon}>👤</Text>
    <Text style={styles.navText}>Mi</Text>
  </TouchableOpacity>
</View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 30,
    marginBottom: 50,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f2027',
  },
  loadingText: {
    color: '#fff',
    marginTop: 10,
    fontSize: 16,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0f2027',
    padding: 20,
  },
  errorText: {
    color: '#ff6347',
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#1e90ff',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: 'rgba(0,0,0,0.3)', // Fondo semi-transparente para el header
  },
  headerIcon: {
    color: '#fff',
    fontSize: 24,
  },
  headerTitle: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
  },
  categoryFilter: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 10,
    backgroundColor: 'rgba(0,0,0,0.2)',
    marginBottom: 10,
    borderRadius: 10,
    marginHorizontal: 10,
  },
  categoryText: {
    color: '#fff',
    fontSize: 16,
    marginRight: 10,
  },
  categoryDropdown: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 8,
  },
  categoryInput: {
    flex: 1,
    color: '#fff',
    fontSize: 16,
  },
  dropdownIcon: {
    color: '#fff',
    fontSize: 16,
    marginLeft: 5,
  },
  listContentContainer: {
    paddingHorizontal: 10,
    paddingBottom: 100, // Espacio para la barra de navegación inferior
  },
  tournamentCard: {
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 10,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  tournamentName: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    flexShrink: 1, // Permite que el texto se encoja si es muy largo
  },
  tournamentStatus: {
    color: '#aaffaa', // Color verde claro para el estado
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 10,
  },
  tournamentDescription: {
    color: '#e0e0e0',
    fontSize: 14,
    marginBottom: 10,
  },
  cardDetails: {
    marginBottom: 10,
  },
  detailText: {
    color: '#ccc',
    fontSize: 13,
    marginBottom: 3,
  },
  streamLink: {
    color: '#1e90ff',
    textDecorationLine: 'underline',
  },
  detailsButton: {
    backgroundColor: '#1e90ff',
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 8,
    alignSelf: 'flex-end', // Alinea el botón a la derecha
    marginTop: 10,
  },
  detailsButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  noTournamentsContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  noTournamentsText: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 20,
  },
  bottomNavBar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.7)',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: 80, // Altura de la barra de navegación
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingBottom: 10, // Espacio para el "safe area" en dispositivos modernos
  },
  navItem: {
    alignItems: 'center',
    padding: 5,
  },
  navIcon: {
    fontSize: 28, // Tamaño del icono (usando emojis como placeholder)
    color: '#fff',
    marginBottom: 4,
  },
  navText: {
    color: '#fff',
    fontSize: 12,
  },
  navPlusButton: {
    backgroundColor: '#1e90ff', // Color del botón central
    width: 60,
    height: 60,
    borderRadius: 30, // Botón circular
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: -30, // Sube el botón por encima de la barra
    shadowColor: '#1e90ff',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 15,
  },
  navPlusIcon: {
    color: '#fff',
    fontSize: 35,
    fontWeight: 'bold',
  },

  
});

