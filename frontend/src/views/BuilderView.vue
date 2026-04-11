<template>
  <div class="builder-page">
    <h1>Smart Mirror Layout Builder</h1>
    <UserProfilePanel
      @update:selected-user-id="selectedUserId = $event"
      @update:selected-profile-name="selectedProfileName = $event"
    />
    <LayoutBuilder :user-id="selectedUserId" :profile-name="selectedProfileName" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import LayoutBuilder from "../components/LayoutBuilder.vue";
import UserProfilePanel from "../components/UserProfilePanel.vue";

const selectedUserId = ref(1);
const selectedProfileName = ref("Default");
</script>

<style scoped>
.builder-page {
  padding: 24px;
  font-family: Arial, sans-serif;
}
</style>