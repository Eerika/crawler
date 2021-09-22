<template>
  <div id="scraper">
    <div id="container" class="w3-container w3-display-middle">
      <div class="w3-panel w3-card">
        <br /><br />
        <h1>Oda Scraper</h1>
        <br /><br />
        <div class="container">
          <div class="row">
            <form v-on:submit.prevent="submitForm" id="input-form" method="post" action="/">
              <input type="radio" id="scraperOptionOda" value="Oda" v-model="form.scraperOption" />
              <label for="oda"> Oda Scraper</label>
              <br />
              <input
                type="radio"
                id="scraperOptionAmazon"
                value="Amazon"
                v-model="form.scraperOption"
              />
              <label for="amazon"> Amazon Scraper</label>
              <br />
              <input
                type="radio"
                id="scraperOptionNotFound"
                value="NotFound"
                v-model="form.scraperOption"
              />
              <label for="notfound"> 404 Scraper</label>
              <br /><br />

              <div class="form-group">
                <label for="url">URL to Scrape </label>
                <input
                  type="text"
                  class="form-control"
                  id="url"
                  placeholder="Input URL"
                  v-model="form.url"
                />
              </div>
              <br />
              <div class="form-group">
                <label for="time">Scrape Time </label>
                <input
                  type="text"
                  class="form-control"
                  id="time"
                  placeholder="10"
                  v-model="form.time"
                />
              </div>

              <br /><br />
              <div class="form-group">
                <button class="btn btn-primary" :disabled="isDisabled">Submit</button>
              </div>
              <br /><br />
              <div class="w3-panel w3-card">
                <div>
                  <b-table striped hover :items="scraped"></b-table>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      form: {
        url: "",
        time: 5,
        scraperOption: "Oda"
      },
      scraped: [],
      scraping: false
    };
  },
  computed: {
    isDisabled() {
      // Check if scraping has finished
      return this.scraping == true;
    }
  },
  methods: {
    submitForm() {
      this.scraping = true;
      this.scraped = [];
      this.doPost();
    },
    doPost() {
      axios
        .post("http://localhost:5000/", this.form)
        .then(res => {
          //Perform Success Action
          console.log("Success!");
          this.getScraped();
        })
        .catch(error => {
          // error.response.status Check status code
          console.log("Error!");
        })
        .finally(() => {
          //Perform action in always
          this.scraping = false;
        });
    },
    getScraped() {
      const path = "http://localhost:5000/output_data";
      axios
        .get(path)
        .then(res => {
          this.scraped = res.data.output_data;
          console.log(res.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>

<style>
#container {
  color: #000000;
  background-color: #ffc17b;
}

#scraperOptionOda {
  margin-right: 10px;
}

#scraperOptionAmazon {
  margin-right: 10px;
}

#scraperOptionNotFound {
  margin-right: 10px;
}
</style>
