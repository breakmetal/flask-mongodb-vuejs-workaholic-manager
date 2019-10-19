<template>
  <v-data-table
    :headers="headers"
    :items="projects"
    sort-by="calories"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Projects</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <v-text-field
        v-model="paramsSearch.search_query"
        append-icon="search"
        label="Search"
        single-line
        :rules="[rules.search]"
        @keyup.enter='filterSearch'
      ></v-text-field>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <div class="flex-grow-1"></div>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">
              <v-icon>note_add</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="4" md="4">
                    <v-text-field v-model="editedItem.title" label="title"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4" md="4">
                    <v-text-field v-model="editedItem.description" label="description"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
       <v-dialog v-model="alertDelete" max-width="290">
              <v-card>
              <v-card-title class="headline">Use Google's location service?</v-card-title>
              <v-card-text>
                are you sure want that remove the project {{editedItem.title}} ? 
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click="alertDelete = false">
                  Disagree
                </v-btn>
                <v-btn color="green darken-1" text @click="deleteItem">
                  Agree
                </v-btn>
              </v-card-actions>
              </v-card>
          </v-dialog>
    </template>
    <template v-slot:item.action="{ item }">
        <v-icon
        small
        class="mr-2"
        @click="viewItem(item)"
      >
        mdi-eye
      </v-icon>
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
       mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="prevDelete(item)"
      >
        mdi-delete-forever
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getProjects">Reset</v-btn>
    </template>
  </v-data-table>
</template>

<script>
import axios from 'axios'
  export default {
    data: () => ({
    alertDelete:false,
    paramsSearch:{
            search_query:'',
            query:'',
            column:'',
            page:1
        },

    rules:{
        search: value => {
          const pattern = /(^(t:[A-Za-z]+))|(d:2\d{3}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])|(^(s:active){1})|(^\s+))/g
          return pattern.test(value) || 'example search by title(t:my project) or created at d:2019-12-31'
      }
     }, 
         
      dialog: false,
      headers: [
        {
          text: 'Title',
          align: 'left',
          sortable: true,
          value: 'title',
        },
        { text: 'Description', value: 'description'},
        { text: 'Status', value: 'status'},
        {
          text: 'Created',
          align: 'left',
          sortable: true,
          value: 'created_at.$date',
        },
        { text: 'Actions', value: 'action', sortable: false },
      ],
      projects: [],
      editedIndex: -1,
      editedItem: {
        title: '',
        description: ''
      },
      defaultItem: {
      },
    }),
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    created () {
      this.getProjects()
    },
    methods: {
        getProjects () {
            axios({ method: 'GET', url: this.buildURL()}).then(
                result => {
                            console.log(result.data)
                            this.projects = result.data
                },
            error => {
                console.error(error)
            })
        },
        editItem (item) {
            this.editedIndex = this.projects.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },
      prevDelete(item){
        this.editedItem = Object.assign({}, item)
        this.alertDelete = true
      },
      deleteItem () {
        this.id = this.editedItem._id.$oid
        axios({ method: 'DELETE', url: `http://127.0.0.1:5000/api/delete_project/${this.id}` }).then(
                result => {
                            console.log(result.data)
                            this.getProjects()

                },
            error => {
                console.error(error)
            })
        this.alertDelete = false
      },
      viewItem(item) {
          this.editedItem = Object.assign({}, item)
          let id = this.editedItem._id.$oid
          this.$router.push(`/project-view/${id}`)
      },
      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      save () {
        if (this.editedIndex == -1) {
          axios.post(`http://127.0.0.1:5000/api/add_project`,this.editedItem).then(
            result => {
                this.isEdit = false
                this.getProjects()
                console.log(result)
          }).catch(err => {
              console.log(err)
          })
        } else {
          this.id = this.editedItem._id.$oid
          axios.put(`http://127.0.0.1:5000/api/update_project/${this.id}`,this.editedItem).then(
            result => {
                this.isEdit = false
                this.getProjects()
                console.log(result)
        }).catch(err => {
            console.log(err)
        })

        }

        this.close() 
      },
      filterSearch() {
        let str=this.paramsSearch.search_query
        let exp =  /(^(t:[A-Za-z]+))|(d:2\d{3}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])|(^(s:active){1}))/g
        if(exp.test(str)){
          let arrayResult=str.split(":")
          this.paramsSearch.column=arrayResult[0]
          this.paramsSearch.query=arrayResult[1]
          this.getProjects()
        }else{
          this.paramsSearch.search_query=""
          this.paramsSearch.page=1
          this.paramsSearch.query=""
          this.getProjects()
        }
      },
       buildURL() {
        var p = this.paramsSearch
        return `http://127.0.0.1:5000/api/list_projects?column=${p.column}&query=${p.query}&page=${p.page}`
    },

    },
  }
</script>