function [errorCode, CurrentNumber, MaximumSamplesNumber] = GatheringCurrentNumberGet(socketId)
%GatheringCurrentNumberGet :  Maximum number of samples and current number during acquisition
%
%	[errorCode, CurrentNumber, MaximumSamplesNumber] = GatheringCurrentNumberGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		int32Ptr CurrentNumber
%		int32Ptr MaximumSamplesNumber


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
CurrentNumber = 0;
MaximumSamplesNumber = 0;

% lib call
[errorCode, CurrentNumber, MaximumSamplesNumber] = calllib('XPS_Q8_drivers', 'GatheringCurrentNumberGet', socketId, CurrentNumber, MaximumSamplesNumber);
