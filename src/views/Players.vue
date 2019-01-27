<template>
    <div class="container">
        <PlayerRankings numResults=10></PlayerRankings>
    </div>
</template>

<script>
// @ is an alias to /src
import store from "@/store.js";
import router from "@/router.js";
import PlayerRankings from "@/components/PlayerRankings.vue";

export default {
    name: "Players",
    components: {
        PlayerRankings
    }
};
</script>