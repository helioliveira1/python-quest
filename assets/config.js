/* Configuração da sincronização na nuvem (Supabase).
   A chave abaixo é a chave PUBLICÁVEL: foi feita para ficar no navegador.
   Quem protege os dados são as regras de RLS no banco (cada usuário só lê e grava a própria linha).
   Para desligar a sincronização, deixe SUPABASE_URL vazio. */
window.PQ_CONFIG = {
  SUPABASE_URL: "https://sjikmkvecgmtrddlgxlf.supabase.co",
  SUPABASE_KEY: "sb_publishable_GbXP_ua1S83QAs3I3I2syQ_FokxytGC"
};
