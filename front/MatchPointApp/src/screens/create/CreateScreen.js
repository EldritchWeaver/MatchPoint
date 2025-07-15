import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Picker } from '@react-native-picker/picker';
import * as api from '../../api/index';

export default function CreateScreen() {
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [categoria, setCategoria] = useState('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [maxEquipos, setMaxEquipos] = useState('');
  const [streamUrl, setStreamUrl] = useState('');
  const [idOrganizador, setIdOrganizador] = useState(''); // Puedes obtenerlo del usuario logueado

  const handleCreate = async () => {
    if (!nombre || !fechaInicio || !fechaFin || !maxEquipos || !idOrganizador) {
      Alert.alert('Error', 'Completa todos los campos obligatorios.');
      return;
    }
    try {
      await api.createTournament({
        nombre,
        descripcion,
        categoria,
        fecha_inicio: fechaInicio,
        fecha_fin: fechaFin,
        max_equipos: maxEquipos,
        stream_url: streamUrl,
        id_organizador: idOrganizador,
        estado: 'programado'
      });
      Alert.alert('Éxito', 'Torneo creado correctamente');
      // Limpia el formulario si quieres
      setNombre('');
      setDescripcion('');
      setCategoria('');
      setFechaInicio('');
      setFechaFin('');
      setMaxEquipos('');
      setStreamUrl('');
    } catch (err) {
      Alert.alert('Error', 'No se pudo crear el torneo');
    }
  };

  return (
    <LinearGradient colors={['#1a2a3a', '#2c5364']} style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Crear Torneo</Text>
        <TextInput
          style={styles.input}
          placeholder="Nombre"
          placeholderTextColor="#ccc"
          value={nombre}
          onChangeText={setNombre}
        />
        <TextInput
          style={styles.input}
          placeholder="Descripción"
          placeholderTextColor="#ccc"
          value={descripcion}
          onChangeText={setDescripcion}
        />
        <Picker
          selectedValue={categoria}
          style={styles.input}
          onValueChange={setCategoria}
        >
          <Picker.Item label="Selecciona categoría" value="" />
          <Picker.Item label="Fútbol" value="futbol" />
          <Picker.Item label="Básquet" value="basquet" />
          {/* Agrega más categorías según tu backend */}
        </Picker>
        <TextInput
          style={styles.input}
          placeholder="Fecha inicio (YYYY-MM-DDTHH:MM:SSZ)"
          placeholderTextColor="#ccc"
          value={fechaInicio}
          onChangeText={setFechaInicio}
        />
        <TextInput
          style={styles.input}
          placeholder="Fecha fin (YYYY-MM-DDTHH:MM:SSZ)"
          placeholderTextColor="#ccc"
          value={fechaFin}
          onChangeText={setFechaFin}
        />
        <TextInput
          style={styles.input}
          placeholder="Máx. equipos"
          placeholderTextColor="#ccc"
          value={maxEquipos}
          onChangeText={setMaxEquipos}
          keyboardType="numeric"
        />
        <TextInput
          style={styles.input}
          placeholder="URL de stream (opcional)"
          placeholderTextColor="#ccc"
          value={streamUrl}
          onChangeText={setStreamUrl}
        />
        <TextInput
          style={styles.input}
          placeholder="ID Organizador"
          placeholderTextColor="#ccc"
          value={idOrganizador}
          onChangeText={setIdOrganizador}
          keyboardType="numeric"
        />
        <Button title="Crear Torneo" onPress={handleCreate} color="#1e90ff" />
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 16 },
  title: { color: '#fff', fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  input: {
    width: '100%',
    backgroundColor: 'rgba(255,255,255,0.15)',
    color: '#fff',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 8,
    fontSize: 16,
    marginBottom: 10,
  },
});