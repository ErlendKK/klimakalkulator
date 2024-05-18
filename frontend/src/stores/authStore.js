import { defineStore } from 'pinia';
import { getData, postData } from '../utils/http-requests.js'


export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    user: null,
    userName: '',
    projects: [],
    currentProject: null
  }),
  actions: {
    logIn(user) {
      console.log(user);
      this.isLoggedIn = true;
      this.user = user;
      this.userName = user.name;
      this.projects = user.projects;
      return true;
    },
    async logOut() {
      await postData({}, '/logout');

      this.isLoggedIn = false;
      this.user = null;
      this.userName = '';
      this.projects = [];
      this.currentProject = null;
    },
    async checkSession() {
      const response = await getData('/session');
      // console.log(response)
      if (response.status === 'success') {
        this.isLoggedIn = true;
        this.user = response;
        this.userName = response.name;
        this.projects = response.projects;

      } else {
        this.isLoggedIn = false;
        this.user = null;
        this.userName = '';
      }
    },
    setCurrentProject(project) {
      this.currentProject = project;
      console.log('setCurrentProject: ', this.currentProject.name);
      console.log(this.currentProject)
    },
    pushToProjects(project) {
      this.projects.push(project);
    },
    pushToProducts(product) {
      this.currentProject.products.push(product);
    },
    popFromProducts(product_id) {
      console.log(`popFromProducts called for id: ${product_id}`);
      this.currentProject.products = this.currentProject.products.filter(p => p.product_id !== product_id);
    },
    popFromProjects(project_id) {
      console.log(`popFromProjects called for id: ${project_id}`);
      if (this.currentProject?.project_id === project_id) {
        this.currentProject = null;
      }

      this.projects = this.projects.filter(p => p.project_id !== project_id);
    },
  }
});