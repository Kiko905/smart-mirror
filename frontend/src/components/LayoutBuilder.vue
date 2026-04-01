<template>
  <div class="layout-builder">
    <div class="sidebar">
      <h2>Available Modules</h2>
      <div
        v-for="module in availableModules"
        :key="module.id"
        class="module-card"
        @click="addModule(module)"
      >
        {{ module.name }}
      </div>
    </div>

    <div class="canvas">
      <h2>User Layout</h2>

      <div v-if="userLayout.length === 0">
        Zatiaľ nie sú pridané žiadne moduly.
      </div>

      <div
        v-for="item in userLayout"
        :key="item.instanceId"
        class="layout-item"
      >
        <strong>{{ item.name }}</strong>
        <div>Module: {{ item.module }}</div>
        <div>Position: {{ item.position }}</div>
        <button @click="removeModule(item.instanceId)">Remove</button>
      </div>

      <div class="actions">
        <button @click="saveLayout">Save Layout</button>
      </div>
    </div>

    <div class="preview">
      <h2>Preview JSON</h2>
      <pre>{{ prettyLayout }}</pre>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import api from "../services/api";
import { onMounted } from "vue";

const availableModules = ref([
  { id: 1, name: "Clock", module: "clock", position: "top_left" },
  { id: 2, name: "Calendar", module: "calendar", position: "top_right" },
  { id: 3, name: "Weather", module: "weather", position: "bottom_left" },
  { id: 4, name: "Newsfeed", module: "newsfeed", position: "bottom_right" },
]);

const userLayout = ref([]);

const addModule = (module) => {
  userLayout.value.push({
    ...module,
    instanceId: `${module.module}-${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 8)}`,
    config: {},
  });
};

const removeModule = (instanceId) => {
  userLayout.value = userLayout.value.filter(
    (item) => item.instanceId !== instanceId
  );
};

const saveLayout = async () => {
  try {
    const payload = {
      profile_name: "Default",
      layout: userLayout.value.map((item) => ({
        module: item.module,
        position: item.position,
        config: item.config || {},
      })),
    };

    await api.post("/mirror-layout/1", payload);
    alert("Layout saved successfully");
  } catch (error) {
    console.error(error);
    alert("Error saving layout");
  }
};

const prettyLayout = computed(() =>
  JSON.stringify(userLayout.value, null, 2)
);

const loadLayout = async () => {
  try {
    const response = await api.get("/mirror-layout/1");

    userLayout.value = response.data.layout.map((module) => ({
      ...module,
      instanceId:
        module.module +
        "-" +
        Date.now() +
        "-" +
        Math.random().toString(36).slice(2, 8),
    }));
  } catch (error) {
    console.log("No saved layout yet");
  }
};

onMounted(() => {
  loadLayout();
});
</script>

<style scoped>
.layout-builder {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 20px;
  padding: 20px;
}

.sidebar,
.canvas,
.preview {
  border: 1px solid #ccc;
  border-radius: 12px;
  padding: 16px;
  background: white;
  color: black;
}

.module-card,
.layout-item {
  background: #f2f2f2;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  cursor: pointer;
}

.actions {
  margin-top: 20px;
}

button {
  margin-top: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
}
</style>