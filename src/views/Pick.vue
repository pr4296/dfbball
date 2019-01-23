<template>
  <div class="container">
        <MakePicks></MakePicks>
    </div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";
import MakePicks from "@/components/MakePicks.vue";

export default {
  name: "home",
  components: {
    MakePicks
  },
  methods: {
    canChangePicks: function() {
        var res = store.state.apiDataCurrentGames.filter(g => g.playedStatus != 'UNPLAYED').length == 0;
        return res;
    },
  },
  created() {
        var hasToken = sessionStorage.getItem('token');
        var canChangePicks = this.canChangePicks();
        if (!hasToken || !canChangePicks) {
            this.$router.replace({ path: "/login" });
            this.$router.go(0);
        }
    }
};
</script>
