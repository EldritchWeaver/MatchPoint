import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ImageBackground, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient'; // Asegúrate de tener esta librería instalada

// Importa tus funciones de API. Ajusta esta ruta según la ubicación real de tu archivo api.js
import * as api from '../../api/index'; // Ejemplo: si este archivo está en src/screens/Auth/RegisterScreen.js

export default function RegisterScreen({ navigation }) {
  const [nombre, setNombre] = useState(''); // Estado para el nombre
  const [nickname, setNickname] = useState(''); // Estado para el nickname
  const [email, setEmail] = useState(''); // Estado para el email
  const [password, setPassword] = useState(''); // Estado para la contraseña
  const [confirmPassword, setConfirmPassword] = useState(''); // Estado para confirmar contraseña
  const [loading, setLoading] = useState(false); // Estado para el indicador de carga

  /**
   * Maneja el proceso de registro de usuario.
   * Llama a la función 'registerUser' de tu archivo api.js.
   */
  const handleRegister = async () => {
    // Validaciones básicas antes de enviar la solicitud
    if (!nombre || !nickname || !email || !password || !confirmPassword) {
      Alert.alert('Error de Registro', 'Por favor, completa todos los campos.');
      return;
    }
    if (password !== confirmPassword) {
      Alert.alert('Error de Registro', 'Las contraseñas no coinciden.');
      return;
    }
    if (password.length < 6) { // Ejemplo de validación de longitud de contraseña
      Alert.alert('Error de Registro', 'La contraseña debe tener al menos 6 caracteres.');
      return;
    }

    setLoading(true); // Activa el estado de carga
    try {
      // Llama a la función de registro de usuario de tu API
      const response = await api.registerUser({ nombre, nickname, email, password });
      
      Alert.alert('Registro Exitoso', '¡Tu cuenta ha sido creada! Ahora puedes iniciar sesión.');
      // Navega a la pantalla de Login después de un registro exitoso
      navigation.navigate('Login');
    } catch (error) {
      // --- INICIO DE MEJORA PARA DIAGNÓSTICO ---
      console.error('Error completo en el registro:', error); // Esto imprimirá el objeto de error completo
      // --- FIN DE MEJORA PARA DIAGNÓSTICO ---

      let errorMessage = 'Error al registrar usuario. Por favor, inténtalo de nuevo.';
      if (error.response) {
        // El servidor respondió con un status code fuera del rango 2xx
        console.error('Error de respuesta del servidor:', error.response.data);
        console.error('Status del servidor:', error.response.status);
        if (error.response.data && error.response.data.detail) {
          errorMessage = error.response.data.detail; // Usa el mensaje de error de la API si está disponible
        } else if (error.response.status === 500) {
          errorMessage = 'Error interno del servidor. Por favor, inténtalo de nuevo más tarde.';
        } else if (error.response.status === 400) {
            errorMessage = 'Datos inválidos. Por favor, revisa tu información.';
        }
      } else if (error.request) {
        // La solicitud fue hecha pero no se recibió respuesta (ej. problema de red, servidor caído)
        console.error('No se recibió respuesta del servidor:', error.request);
        errorMessage = 'No se pudo conectar al servidor. Verifica tu conexión o la URL de la API.';
      } else {
        // Algo más causó el error al configurar la solicitud
        console.error('Error al configurar la solicitud:', error.message);
        errorMessage = 'Ocurrió un error inesperado. Inténtalo de nuevo.';
      }
      Alert.alert('Error de Registro', errorMessage);
    } finally {
      setLoading(false); // Desactiva el estado de carga
    }
  };

  return (
    // Contenedor principal con imagen de fondo
    <ImageBackground
      source={{ uri: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80' }}
      style={styles.background}
      resizeMode="cover"
    >
      {/* Capa superpuesta para mejorar la legibilidad del texto */}
      <View style={styles.overlay}>
        {/* Título de la pantalla de registro */}
        <Text style={styles.title}>Crear Cuenta</Text>

        {/* Campo de entrada para el nombre */}
        <TextInput
          style={styles.input}
          placeholder="Nombre Completo"
          placeholderTextColor="#ccc"
          value={nombre}
          onChangeText={setNombre}
          autoCapitalize="words" // Capitaliza la primera letra de cada palabra
        />

        {/* Campo de entrada para el nickname */}
        <TextInput
          style={styles.input}
          placeholder="Nickname"
          placeholderTextColor="#ccc"
          value={nickname}
          onChangeText={setNickname}
          autoCapitalize="none" // No capitaliza automáticamente
        />

        {/* Campo de entrada para el correo electrónico */}
        <TextInput
          style={styles.input}
          placeholder="Correo Electrónico"
          placeholderTextColor="#ccc"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address" // Teclado optimizado para emails
        />

        {/* Campo de entrada para la contraseña */}
        <TextInput
          style={styles.input}
          placeholder="Contraseña"
          placeholderTextColor="#ccc"
          value={password}
          onChangeText={setPassword}
          secureTextEntry // Oculta el texto ingresado
        />

        {/* Campo de entrada para confirmar contraseña */}
        <TextInput
          style={styles.input}
          placeholder="Confirmar Contraseña"
          placeholderTextColor="#ccc"
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          secureTextEntry // Oculta el texto ingresado
        />

        {/* Botón de registro con gradiente lineal */}
        <LinearGradient colors={["#0f2027", "#2c5364"]} style={styles.button}>
          <TouchableOpacity onPress={handleRegister} disabled={loading} style={styles.buttonTouchable}>
            <Text style={styles.buttonText}>
              {loading ? 'Registrando...' : 'Registrarse'}
            </Text>
          </TouchableOpacity>
        </LinearGradient>

        {/* Enlace para volver al inicio de sesión */}
        <TouchableOpacity onPress={() => navigation.navigate('Login')}>
          <Text style={styles.link}>¿Ya tienes cuenta? Inicia Sesión</Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
}

// Estilos (pueden ser compartidos o adaptados de LoginScreen)
const styles = StyleSheet.create({
  background: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 30,
    marginBottom: 50,
  },
  overlay: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    width: 320,
    borderRadius: 24,
    padding: 24,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.5,
    shadowRadius: 10,
    elevation: 10,
  },
  title: {
    color: '#fff',
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 32,
    marginTop: 8,
  },
  input: {
    width: '100%',
    backgroundColor: '#222',
    color: '#fff',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
    fontSize: 16,
  },
  button: {
    width: '100%',
    borderRadius: 8,
    marginBottom: 16,
    overflow: 'hidden',
  },
  buttonTouchable: {
    width: '100%',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 18,
    paddingVertical: 12,
  },
  link: {
    color: '#1e90ff',
    fontSize: 15,
    marginTop: 4,
    textDecorationLine: 'underline',
  },
});

