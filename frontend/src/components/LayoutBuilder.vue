<template>
  <div class="layout-builder">
    <div class="sidebar">
      <h2>Available Modules</h2>

      <VueDraggableNext
        :list="availableModules"
        :group="{ name: 'modules', pull: 'clone', put: false }"
        item-key="id"
        :sort="false"
        :clone="cloneModule"
      >
        <div v-for="item in availableModules" :key="item.id" class="module-card">
          <div class="module-title">{{ item.name }}</div>
          <div class="module-description">{{ item.description }}</div>
        </div>
      </VueDraggableNext>
    </div>

    <div class="canvas">
      <h2>User Layout</h2>

      <VueDraggableNext
        v-model="userLayout"
        group="modules"
        item-key="instanceId"
        class="drop-zone"
      >
        <div v-for="(item, index) in userLayout" :key="item.instanceId" class="layout-item">
          <div class="layout-header">
            <strong>{{ item.name }}</strong>
            <span class="module-tag">{{ item.module }}</span>
          </div>

          <div class="field-group">
            <label>Pozícia</label>
            <select v-model="item.position">
              <option value="top_left">top_left</option>
              <option value="top_center">top_center</option>
              <option value="top_right">top_right</option>
              <option value="upper_third">upper_third</option>
              <option value="middle_center">middle_center</option>
              <option value="lower_third">lower_third</option>
              <option value="bottom_left">bottom_left</option>
              <option value="bottom_center">bottom_center</option>
              <option value="bottom_right">bottom_right</option>
              <option value="bottom_bar">bottom_bar</option>
            </select>
          </div>

          <div class="actions-row">
            <button @click="removeModule(item.instanceId)">Remove</button>
            <span class="order-info">Poradie: {{ index + 1 }}</span>
          </div>
        </div>
      </VueDraggableNext>

      <div v-if="userLayout.length === 0" class="empty-state">
        Potiahni modul sem.
      </div>

      <div class="main-actions">
        <button class="save-btn" @click="saveLayout">Save Layout</button>
      </div>
    </div>

    <div class="preview">
      <h2>Preview JSON</h2>
      <pre>{{ prettyLayout }}</pre>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { VueDraggableNext } from 'vue-draggable-next';
import api from "../services/api";

const availableModules = ref([
  {
    id: 1,
    name: "Clock",
    module: "clock",
    position: "top_left",
    description: "Zobrazí aktuálny čas.",
  },
  {
    id: 2,
    name: "Calendar",
    module: "calendar",
    position: "top_left",
    description: "Kalendár a sviatky.",
  },
  {
    id: 3,
    name: "Weather",
    module: "weather",
    position: "top_right",
    description: "Aktuálne počasie.",
  },
  {
    id: 4,
    name: "Newsfeed",
    module: "newsfeed",
    position: "bottom_bar",
    description: "Novinky z RSS feedu.",
  },
  {
    id: 5,
    name: "Compliments",
    module: "compliments",
    position: "lower_third",
    description: "Textové hlášky na obrazovke.",
  },
]);

const moduleDisplayNames = {
  clock: "Clock",
  calendar: "Calendar",
  weather: "Weather",
  newsfeed: "Newsfeed",
  compliments: "Compliments",
};

const userLayout = ref([]);

const cloneModule = (module) => {
  return {
    name: module.name,
    module: module.module,
    position: module.position,
    config: {},
    instanceId: `${module.module}-${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 8)}`,
  };
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

    console.log("SAVING PAYLOAD:", payload);

    await api.post("/mirror-layout/1", payload);
    alert("Layout saved successfully");
  } catch (error) {
    console.error(error);
    alert("Error saving layout");
  }
};

const loadLayout = async () => {
  try {
    const response = await api.get("/mirror-layout/1");

    userLayout.value = response.data.layout.map((module) => ({
      ...module,
      name: moduleDisplayNames[module.module] || module.module,
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

const prettyLayout = computed(() =>
  JSON.stringify(
    userLayout.value.map((item) => ({
      module: item.module,
      position: item.position,
      config: item.config,
    })),
    null,
    2
  )
);
</script>

<style scoped>
.layout-builder {
  display: grid;
  grid-template-columns: 1fr 2fr 1.2fr;
  gap: 20px;
  padding: 20px;
  background: #f7f8fb;
  min-height: 100vh;
  box-sizing: border-box;
}

.sidebar,
.canvas,
.preview {
  background: white;
  border: 1px solid #e4e7ec;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
}

h2 {
  margin-top: 0;
  margin-bottom: 16px;
}

.module-card {
  background: #f3f4f6;
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 12px;
  cursor: grab;
  transition: 0.2s ease;
}

.module-card:hover {
  background: #e8edf5;
  transform: translateY(-1px);
}

.module-title {
  font-weight: 700;
  margin-bottom: 6px;
}

.module-description {
  font-size: 14px;
  color: #555;
}

.drop-zone {
  min-height: 250px;
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 12px;
  background: #fafafa;
}

.empty-state {
  color: #777;
  padding: 16px 0;
}

.layout-item {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 14px;
  background: white;
}

.layout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.module-tag {
  font-size: 12px;
  background: #e9eef8;
  color: #334155;
  padding: 4px 8px;
  border-radius: 999px;
}

.field-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}

.field-group label {
  font-size: 14px;
  margin-bottom: 6px;
  color: #374151;
}

select {
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.actions-row,
.main-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.main-actions {
  margin-top: 20px;
}

button {
  padding: 9px 14px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  background: #e5e7eb;
  transition: 0.2s ease;
}

button:hover:enabled {
  background: #dbe1e8;
}

.save-btn {
  background: #2563eb;
  color: white;
}

.save-btn:hover {
  background: #1d4ed8;
}

.order-info {
  font-size: 13px;
  color: #64748b;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
  background: #0f172a;
  color: #e2e8f0;
  padding: 14px;
  border-radius: 12px;
  overflow: auto;
}
</style>