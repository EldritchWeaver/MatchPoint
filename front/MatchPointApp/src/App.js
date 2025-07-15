import React from 'react';
import { NavigationContainer } from '@react-navigation/native'; // Contenedor principal de navegación
import { createNativeStackNavigator } from '@react-navigation/native-stack'; // Navegador de pila nativo

// Importa tus pantallas
import ConfigScreen from './screens/config/configscreen';
import LoginScreen from './screens/Auth/LoginScreen'; // Asegúrate que esta ruta sea correcta
import HomeScreen from './screens/Home/HomeScreen'; // Descomenta si tienes una pantalla Home
import RegisterScreen from './screens/Auth/RegisterScreen';
import ExploreScreen from './screens/explore/ExploreScreen';
import ChatScreen from './screens/chat/ChatScreen';
import CreateScreen from './screens/create/CreateScreen';
// OJO: El archivo de perfil tiene un espacio en el nombre (no pregunten por que), así que:
import ProfileScreen from './screens/profile/Profile Screen';


const Stack = createNativeStackNavigator(); // Crea una instancia del navegador de pila

export default function App() {
  return (
    // NavigationContainer es el componente que envuelve toda la estructura de navegación
    <NavigationContainer>
      {/* Stack.Navigator define el navegador de pila */}
      <Stack.Navigator initialRouteName="Login">
        {/* Stack.Screen define cada pantalla en la pila */}
        {/* La pantalla de Login es la ruta inicial */}
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ headerShown: false }} // Oculta el encabezado para la pantalla de login
        />
        {/* La pantalla de Registro, con el encabezado oculto para consistencia */}
        <Stack.Screen
          name="Register"
          component={RegisterScreen}
          options={{ headerShown: false }} // Oculta el encabezado para la pantalla de registro
        />

        {/* Puedes añadir más pantallas aquí, por ejemplo: */}
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Inicio', headerShown: false }} // Título del encabezado para la pantalla Home
        />
        <Stack.Screen
          name="Explore"
          component={ExploreScreen}
          options={{ title: 'Explorar', headerShown: false }}
        />
        <Stack.Screen
          name="Chat"
          component={ChatScreen}
          options={{ title: 'Chat', headerShown: false }}
        />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={{ title: 'Mi Perfil', headerShown: false }}
        />
        <Stack.Screen
          name="Create"
          component={CreateScreen}
          options={{ title: 'Crear', headerShown: false }}
    
        />
<Stack.Screen
  name="Config"
  component={ConfigScreen}
  options={{ title: 'Configuración', headerShown: false }}
/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}

