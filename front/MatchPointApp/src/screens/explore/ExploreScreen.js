import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, FlatList, TextInput } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as api from '../../api/index';
import { Picker } from '@react-native-picker/picker';

export default function ExploreScreen() {
  const [tournaments, setTournaments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchText, setSearchText] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  const filteredTournaments = tournaments.filter(t =>
    (selectedCategory === '' || t.categoria === selectedCategory) &&
    (
      t.nombre.toLowerCase().includes(searchText.toLowerCase()) ||
      (t.descripcion && t.descripcion.toLowerCase().includes(searchText.toLowerCase()))
    )
  );

  useEffect(() => {
    api.listTournamentsByStatus('programado')
      .then(res => setTournaments(res.data))
      .catch(() => setTournaments([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <LinearGradient
      colors={['#1a2a3a', '#2c5364']}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.container}
    >
      <View style={styles.content}>
        <View style={{ flexDirection: 'row', marginBottom: 10 }}>
          <TextInput
            style={{
              flex: 1,
              backgroundColor: 'rgba(255,255,255,0.15)',
              color: '#fff',
              borderRadius: 8,
              paddingHorizontal: 12,
              fontSize: 16,
              marginRight: 8,
            }}
            placeholder="Buscar torneo..."
            placeholderTextColor="#ccc"
            value={searchText}
            onChangeText={setSearchText}
          />
          <Picker
            selectedValue={selectedCategory}
            style={{ width: 130, color: '#fff', backgroundColor: 'rgba(255,255,255,0.15)' }}
            dropdownIconColor="#fff"
            onValueChange={setSelectedCategory}
          >
            <Picker.Item label="Todas" value="" />
            <Picker.Item label="Fútbol" value="futbol" />
            <Picker.Item label="Básquet" value="basquet" />
            {/* Agrega más categorías según tu backend */}
          </Picker>
        </View>
        {loading ? (
          <ActivityIndicator color="#fff" size="large" />
        ) : (
          <FlatList
            data={filteredTournaments}
            keyExtractor={item => item.id.toString()}
            renderItem={({ item }) => (
              <View style={styles.tournamentCard}>
                <Text style={styles.tournamentName}>{item.nombre}</Text>
                <Text style={styles.tournamentDesc}>{item.descripcion}</Text>
                <Text style={styles.tournamentCat}>Categoría: {item.categoria}</Text>
                <Text style={styles.tournamentCat}>Estado: {item.estado}</Text>
                <Text style={styles.tournamentCat}>Inicio: {new Date(item.fecha_inicio).toLocaleString()}</Text>
                <Text style={styles.tournamentCat}>Fin: {new Date(item.fecha_fin).toLocaleString()}</Text>
                <Text style={styles.tournamentCat}>Equipos Máx: {item.max_equipos}</Text>
                {item.stream_url && (
                  <Text style={styles.tournamentCat}>Stream: <Text style={{ color: '#1e90ff' }}>{item.stream_url}</Text></Text>
                )}
              </View>
            )}
          />
        )}
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { flex: 1, padding: 16 },
  tournamentCard: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 10,
    padding: 12,
    marginBottom: 10,
  },
  tournamentName: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  tournamentDesc: { color: '#e0e0e0', fontSize: 14 },
  tournamentCat: { color: '#1e90ff', fontSize: 13, marginTop: 4 },
});