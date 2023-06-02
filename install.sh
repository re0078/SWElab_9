set -e

cd users && docker build -t user-service .
cd ..

cd products && docker build -t products-service .
cd ..

cd orders && docker build -t order-service .

docker run -d --name user-service -p 5000:5000 user-service

docker run -d --name products-service -p 5001:5000 products-service

docker run -d --name order-service -p 5002:5000 --link user-service:user-service order-service

