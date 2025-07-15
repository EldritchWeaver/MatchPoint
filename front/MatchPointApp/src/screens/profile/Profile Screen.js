import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as api from '../../api/index';

export default function ProfileScreen({ route }) {
  const nickname = route?.params?.nickname || 'mi_nickname';

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getUserByNickname(nickname)
      .then(res => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, [nickname]);

  return (
    <LinearGradient colors={['#1a2a3a', '#2c5364']} style={styles.container}>
      <View style={styles.content}>
        {loading ? (
          <ActivityIndicator color="#fff" size="large" />
        ) : user ? (
          <>
            <Text style={styles.text}>Nombre: {user.nombre}</Text>
            <Text style={styles.text}>Nickname: {user.nickname}</Text>
            <Text style={styles.text}>Email: {user.email}</Text>
          </>
        ) : (
          <Text style={styles.text}>No se pudo cargar el perfil</Text>
        )}
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  text: { color: '#fff', fontSize: 20, marginBottom: 10 },
});