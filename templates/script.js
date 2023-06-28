window.addEventListener('DOMContentLoaded', () => {
    const cropListElement = document.getElementById('cropList');
    const additionalInfoElement = document.getElementById('additionalInfo');
    
    // Simulated data or fetch recommendations from backend API
    const recommendedCrops = ['Wheat', 'Corn', 'Soybean'];
    
    // Generate the crop list dynamically
    recommendedCrops.forEach(crop => {
      const listItem = document.createElement('li');
      listItem.textContent = crop;
      cropListElement.appendChild(listItem);
    });
    
    // Simulated additional information or fetch from backend API
    const additionalInfo = 'Based on the input parameters, we recommend the above crops for optimal growth and yield in your region.';
    additionalInfoElement.textContent = additionalInfo;
  });
  