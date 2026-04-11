<template>
  <div class="user-panel">
    <div class="panel-card">
      <h2>Users</h2>

      <div class="row">
        <label for="userSelect">Selected user</label>
        <select id="userSelect" v-model.number="selectedUserId">
          <option
            v-for="user in users"
            :key="user.id"
            :value="user.id"
          >
            {{ user.name }} ({{ user.email }})
          </option>
        </select>
      </div>

      <div v-if="selectedUser" class="status-row">
        <span class="chip" :class="selectedUser.has_face_encoding ? 'ok' : 'warn'">
          Face: {{ selectedUser.has_face_encoding ? "configured" : "missing" }}
        </span>
        <span class="chip" :class="selectedUser.voice_enabled ? 'ok' : 'warn'">
          Voice: {{ selectedUser.voice_enabled ? "enabled" : "disabled" }}
        </span>
        <span class="chip" :class="selectedUser.voice_mock_mode ? 'warn' : 'ok'">
          Voice mode: {{ selectedUser.voice_mock_mode ? "mock" : "real" }}
        </span>
      </div>

      <div class="row two-cols">
        <div>
          <label>Name</label>
          <input v-model="editUser.name" type="text" />
        </div>
        <div>
          <label>Email</label>
          <input v-model="editUser.email" type="email" />
        </div>
      </div>

      <div class="actions">
        <button @click="saveUser">Save user</button>
        <button class="secondary" @click="addMockFaceEncoding">Add mock face encoding</button>
      </div>
    </div>

    <div class="panel-card">
      <h2>Profiles</h2>

      <div class="row two-cols">
        <div>
          <label>New profile name</label>
          <input v-model="newProfileName" type="text" placeholder="Default" />
        </div>
        <div class="align-end">
          <button @click="createProfile">Create profile</button>
        </div>
      </div>

      <div class="profile-list">
        <div v-for="profile in profiles" :key="profile.id" class="profile-item">
          <div>
            <strong>{{ profile.profile_name }}</strong>
            <span class="meta">{{ profile.has_layout ? "layout ready" : "no layout" }}</span>
          </div>
          <div class="actions">
            <span v-if="profile.is_active" class="chip ok">Active</span>
            <button v-else class="secondary" @click="activateProfile(profile.id)">Activate</button>
          </div>
        </div>
      </div>
    </div>

    <div class="panel-card">
      <h2>Create User</h2>
      <div class="row two-cols">
        <div>
          <label>Name</label>
          <input v-model="createUser.name" type="text" />
        </div>
        <div>
          <label>Email</label>
          <input v-model="createUser.email" type="email" />
        </div>
      </div>
      <div class="actions">
        <button @click="createNewUser">Create user</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import api from "../services/api";

const emit = defineEmits(["update:selectedUserId", "update:selectedProfileName"]);

const users = ref([]);
const profiles = ref([]);
const selectedUserId = ref(null);
const selectedUser = computed(() => users.value.find((user) => user.id === selectedUserId.value));

const editUser = ref({ name: "", email: "" });
const createUser = ref({ name: "", email: "" });
const newProfileName = ref("Default");

const hydrateSelectedUser = () => {
  if (!selectedUser.value) {
    return;
  }

  editUser.value = {
    name: selectedUser.value.name,
    email: selectedUser.value.email,
  };
};

const fetchUsers = async () => {
  const response = await api.get("/users");
  users.value = response.data.data;

  if (!selectedUserId.value && users.value.length > 0) {
    selectedUserId.value = users.value[0].id;
  }

  hydrateSelectedUser();
};

const fetchProfiles = async () => {
  if (!selectedUserId.value) {
    profiles.value = [];
    return;
  }

  const response = await api.get(`/users/${selectedUserId.value}/mirror-profiles`);
  profiles.value = response.data.data;

  const activeProfile = profiles.value.find((profile) => profile.is_active) || profiles.value[0];
  emit("update:selectedProfileName", activeProfile?.profile_name || "Default");
};

const saveUser = async () => {
  if (!selectedUserId.value) {
    return;
  }

  await api.put(`/users/${selectedUserId.value}`, editUser.value);
  await fetchUsers();
  alert("User updated");
};

const createNewUser = async () => {
  if (!createUser.value.name || !createUser.value.email) {
    alert("Name and email are required");
    return;
  }

  await api.post("/users", createUser.value);
  createUser.value = { name: "", email: "" };
  await fetchUsers();
  alert("User created");
};

const createProfile = async () => {
  if (!selectedUserId.value || !newProfileName.value) {
    return;
  }

  await api.post(`/users/${selectedUserId.value}/mirror-profiles`, {
    profile_name: newProfileName.value,
    is_active: false,
  });

  await fetchProfiles();
  alert("Profile created");
};

const activateProfile = async (profileId) => {
  await api.patch(`/mirror-profiles/${profileId}/activate`);
  await fetchProfiles();
  alert("Profile activated");
};

const generateMockEncoding = () => {
  return Array.from({ length: 16 }, () => Number(Math.random().toFixed(4)));
};

const addMockFaceEncoding = async () => {
  if (!selectedUserId.value) {
    return;
  }

  await api.post(`/users/${selectedUserId.value}/face-encodings`, {
    encoding: generateMockEncoding(),
    image_path: "mock://local-face-sample",
  });

  await fetchUsers();
  alert("Mock face encoding added");
};

watch(selectedUserId, async (userId) => {
  if (!userId) {
    return;
  }

  emit("update:selectedUserId", userId);
  hydrateSelectedUser();
  await fetchProfiles();
});

onMounted(async () => {
  await fetchUsers();
  if (selectedUserId.value) {
    emit("update:selectedUserId", selectedUserId.value);
    await fetchProfiles();
  }
});
</script>

<style scoped>
.user-panel {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 18px;
}

.panel-card {
  background: white;
  border: 1px solid #e4e7ec;
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
}

h2 {
  margin-top: 0;
  margin-bottom: 14px;
}

.row {
  margin-bottom: 12px;
}

.two-cols {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.align-end {
  display: flex;
  align-items: flex-end;
}

label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #374151;
}

input,
select {
  width: 100%;
  box-sizing: border-box;
  padding: 9px 10px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
}

.status-row,
.actions {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  background: #2563eb;
  color: white;
}

button.secondary {
  background: #e5e7eb;
  color: #111827;
}

.chip {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 999px;
}

.chip.ok {
  background: #dcfce7;
  color: #166534;
}

.chip.warn {
  background: #fef3c7;
  color: #92400e;
}

.profile-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-item {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.meta {
  display: block;
  font-size: 12px;
  color: #6b7280;
}

@media (max-width: 1100px) {
  .user-panel {
    grid-template-columns: 1fr;
  }
}
</style>
