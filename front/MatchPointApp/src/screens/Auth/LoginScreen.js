import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ImageBackground, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

// Importa tus funciones de API. Asegúrate de que la ruta sea correcta en tu proyecto.
import * as api from '../../api/index'; // Ajusta esta ruta según la ubicación real de tu archivo api.js

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState(''); // Estado para el input de email
  const [password, setPassword] = useState(''); // Estado para el input de contraseña
  const [loading, setLoading] = useState(false); // Estado para el indicador de carga

  /**
   * Maneja el proceso de inicio de sesión.
   * Llama a la función 'login' de tu archivo api.js.
   */
  const handleLogin = async () => {
    setLoading(true); // Activa el estado de carga
    try {
      // Llama a la función de login de tu API
      const response = await api.login({ email, password });
      
      // Si el login es exitoso (la promesa se resuelve)
      // Puedes guardar el token de autenticación si tu API lo devuelve
      // api.setAuthToken(response.data.access_token); // Descomenta si necesitas guardar el token globalmente
      
      Alert.alert('Login exitoso', '¡Bienvenido!');
      // Aquí puedes navegar a la pantalla principal o realizar otras acciones post-login
      navigation.navigate('Home');

    } catch (error) {
      // --- INICIO DE MEJORA PARA DIAGNÓSTICO ---
      // Esto imprimirá el objeto de error completo en la terminal de Expo
      console.error('Error en el login:', error); 
      // --- FIN DE MEJORA PARA DIAGNÓSTICO ---

      let errorMessage = 'Error al iniciar sesión. Por favor, inténtalo de nuevo.';
      if (error.response) {
        // El servidor respondió con un status code fuera del rango 2xx
        console.error('Error de respuesta del servidor:', error.response.data);
        console.error('Status del servidor:', error.response.status);
        if (error.response.data && error.response.data.detail) {
          // Usa el mensaje de error de la API si está disponible
          errorMessage = error.response.data.detail; 
        } else if (error.response.status === 401) {
          errorMessage = 'Credenciales incorrectas.';
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
      Alert.alert('Error de Login', errorMessage);
    } finally {
      setLoading(false); // Desactiva el estado de carga
    }
  };

  /**
   * Maneja la acción de "Olvidé mi contraseña".
   * Muestra una alerta indicando que la funcionalidad no está implementada.
   */
  const handleForgotPassword = () => {
    Alert.alert('Recuperar contraseña', 'Funcionalidad no implementada aún.');
  };

  /**
   * Maneja la acción de "Registrarse".
   * Navega a la pantalla de registro.
   */
  const handleRegister = () => {
    navigation.navigate('Register'); // Solo navega
  };

  return (
    // Contenedor principal con imagen de fondo
    <ImageBackground
      source={{ uri: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80' }} // URL de la imagen de fondo
      style={styles.background}
      resizeMode="cover" // Ajusta la imagen para cubrir el área
    >
      {/* Capa superpuesta para mejorar la legibilidad del texto */}
      <View style={styles.overlay}>
        {/* Título de la pantalla de inicio de sesión */}
        <Text style={styles.title}>Inicio de Sesión</Text>

        {/* Campo de entrada para el correo electrónico */}
        <TextInput
          style={styles.input}
          placeholder="Correo Electrónico"
          placeholderTextColor="#ccc" // Color del texto del placeholder
          value={email}
          onChangeText={setEmail} // Actualiza el estado del email
          autoCapitalize="none" // Evita la capitalización automática
          keyboardType="email-address" // Teclado optimizado para emails
        />

        {/* Campo de entrada para la contraseña */}
        <TextInput
          style={styles.input}
          placeholder="Contraseña"
          placeholderTextColor="#ccc" // Color del texto del placeholder
          value={password}
          onChangeText={setPassword} // Actualiza el estado de la contraseña
          secureTextEntry // Oculta el texto ingresado (para contraseñas)
        />

        {/* Botón de inicio de sesión con gradiente lineal */}
        <LinearGradient colors={["#0f2027", "#2c5364"]} style={styles.button}>
          <TouchableOpacity onPress={handleLogin} disabled={loading} style={styles.buttonTouchable}>
            <Text style={styles.buttonText}>
              {loading ? 'Entrando...' : 'Entrar'} {/* Cambia el texto si está cargando */}
            </Text>
          </TouchableOpacity>
        </LinearGradient>

        {/* Enlace para "Olvidé mi contraseña" */}
        <TouchableOpacity onPress={handleForgotPassword}>
          <Text style={styles.link}>Olvidé mi contraseña</Text>
        </TouchableOpacity>

        {/* Enlace para "Registrarse" */}
        <TouchableOpacity onPress={handleRegister}>
          <Text style={styles.link}>Registrarse</Text>
        </TouchableOpacity>
      </View>
    </ImageBackground>
  );
}

// Estilos para los componentes de React Native
const styles = StyleSheet.create({
  background: {
    flex: 1, // Ocupa todo el espacio disponible
    justifyContent: 'center', // Centra el contenido verticalmente
    alignItems: 'center', // Centra el contenido horizontalmente
    marginTop: 30,
    marginBottom: 50,
  },
  overlay: {
    backgroundColor: 'rgba(0,0,0,0.7)', // Fondo semi-transparente
    width: 320, // Ancho fijo del contenedor de formulario
    borderRadius: 24, // Bordes redondeados
    padding: 24, // Espaciado interno
    alignItems: 'center', // Centra los elementos dentro del overlay
    shadowColor: '#000', // Color de la sombra
    shadowOffset: { width: 0, height: 4 }, // Desplazamiento de la sombra
    shadowOpacity: 0.5, // Opacidad de la sombra
    shadowRadius: 10, // Radio de desenfoque de la sombra
    elevation: 10, // Elevación para Android (simula sombra)
  },
  title: {
    color: '#fff', // Color del texto del título
    fontSize: 28, // Tamaño de fuente
    fontWeight: 'bold', // Peso de la fuente
    marginBottom: 32, // Margen inferior
    marginTop: 8, // Margen superior
  },
  input: {
    width: '100%', // Ocupa todo el ancho disponible
    backgroundColor: '#222', // Color de fondo del input
    color: '#fff', // Color del texto del input
    borderRadius: 8, // Bordes redondeados
    padding: 12, // Espaciado interno
    marginBottom: 16, // Margen inferior
    fontSize: 16, // Tamaño de fuente
  },
  button: {
    width: '100%', // Ocupa todo el ancho disponible
    borderRadius: 8, // Bordes redondeados
    marginBottom: 16, // Margen inferior
    overflow: 'hidden', // Asegura que el gradiente no se salga de los bordes
  },
  buttonTouchable: {
    width: '100%', // Asegura que el TouchableOpacity ocupe todo el espacio del gradiente
    alignItems: 'center', // Centra el texto del botón
  },
  buttonText: {
    color: '#fff', // Color del texto del botón
    fontWeight: 'bold', // Peso de la fuente
    fontSize: 18, // Tamaño de fuente
    paddingVertical: 12, // Espaciado vertical interno
  },
  link: {
    color: '#1e90ff', // Color del enlace
    fontSize: 15, // Tamaño de fuente
    marginTop: 4, // Margen superior
    textDecorationLine: 'underline', // Subrayado del texto
  },
});

