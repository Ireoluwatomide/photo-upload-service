import { useState, useEffect } from "react";
import { ChakraProvider, Heading, Center, VStack, 
         Text, HStack, Button, SimpleGrid, Image, Spinner} from "@chakra-ui/react";

export default function App() {

  const [allPhotos, setAllPhotos] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isSelected, setIsSelected] = useState(false);
  const [uploadSuccessful, setUploadSuccessful] = useState(false);
  const [showSpinner, setShowSpinner] = useState(false);



  const onInputChange = (event) => {
    setIsSelected(true);
    setSelectedFile(event.target.files[0]);
  };

  const onFileUpload = () => {
    setShowSpinner(true);
    const formData = new FormData();
    formData.append("file", selectedFile, selectedFile.name);
    fetch("http://localhost:8080/photos", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setUploadSuccessful(!uploadSuccessful);
        setShowSpinner(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setShowSpinner(false);
      });
  };

  useEffect(() => {
    fetch("http://localhost:8080/photos")
      .then((response) => response.json())
      .then((data) => {console.log(data);
      setAllPhotos(data);
    });
  }, [uploadSuccessful]);

  return  (
    <ChakraProvider>
      <Center bg="black" color="white" padding={8}>
        <VStack spacing={7}>
          <Heading size="2xl">Your Gallery</Heading>
          <Text fontSize="xl">Take a look at all your photos!</Text>
          <HStack>
            <input type="file" onChange={onInputChange} onClick={null}></input>
            <Button size="lg" colorScheme="red" isDisabled={!isSelected} onClick={onFileUpload}>Upload Photo</Button>
            {
              showSpinner && (
                <Center><Spinner size="xl"></Spinner></Center>
              )
            }
          </HStack>
          <Heading size="lg">Your Photos</Heading>
          <SimpleGrid columns={4} spacing={8}>
            {
              allPhotos.map((photo) => {
                return (
                  <Image borderRadius={25} boxSize="300px" src={photo["photo_url"]} 
                  fallbackSrc="https://via.placeholder.com/300"objectFit="cover"></Image>
                )
              })
            }
          </SimpleGrid>
        </VStack>
      </Center>
    </ChakraProvider>
  );
}