FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

COPY . .

# The flag is generated in app.js at runtime at /flag.txt

EXPOSE 3000

CMD ["npm", "start"]
