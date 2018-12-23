<template>
  <div class="container">
        <CurrentGames></CurrentGames>
        <DailyTopPlayers forteam="all"></DailyTopPlayers>
    </div>
</template>

<script>

import CurrentGames from "@/components/CurrentGames.vue";
import DailyTopPlayers from "@/components/DailyTopPlayers.vue";

export default {
  name: "home",
  components: {
    CurrentGames,
    DailyTopPlayers
  }
};
</script>
